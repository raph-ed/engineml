# backend.py

import datetime
import warnings
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
from scipy.stats import norm
from scipy.optimize import minimize
from sklearn.covariance import LedoitWolf
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

try:
    from catboost import CatBoostClassifier
    HAS_CAT = True
except ImportError:
    HAS_CAT = False


# =====================================================================
# 1. COLLECTE DE DONNÉES & GÉNÉRATEUR STOCHASTIQUE DE MARKOV (BUFFER 400J)
# =====================================================================

def _generate_markov_fallback(tickers, fetch_start, end_dt):
    """Génère des séries réalistes à 3 états de Markov si yfinance échoue ou en mode démo."""
    rng = np.random.default_rng(42)
    dates = pd.bdate_range(start=fetch_start, end=end_dt)
    n = len(dates)

    # Matrice de transition Markov (0: Bull, 1: Neutral, 2: Crisis)
    trans = np.array([
        [0.95, 0.04, 0.01],
        [0.05, 0.92, 0.03],
        [0.04, 0.08, 0.88]
    ])
    states = np.zeros(n, dtype=int)
    for t in range(1, n):
        states[t] = rng.choice([0, 1, 2], p=trans[states[t - 1]])

    mu_map = {0: 0.0008, 1: 0.0001, 2: -0.0022}
    vol_map = {0: 0.0085, 1: 0.0105, 2: 0.0240}

    data = {}
    spy_rets = np.array([rng.normal(mu_map[s], vol_map[s]) for s in states])
    data["SPY"] = 450.0 * np.exp(np.cumsum(spy_rets))

    for tk in tickers:
        if tk == "SPY":
            continue
        elif tk in ["QQQ", "EZU", "VGK"]:
            beta = 1.18 if tk == "QQQ" else 0.92
            r = beta * spy_rets + rng.normal(0, 0.004, n)
            data[tk] = 350.0 * np.exp(np.cumsum(r))
        elif tk in ["TLT", "SHY", "GLD"]:
            corr = -0.35 if tk == "TLT" else (-0.15 if tk == "GLD" else -0.05)
            v_scale = 0.007 if tk != "SHY" else 0.0015
            r = corr * spy_rets + rng.normal(0.0002, v_scale, n)
            data[tk] = 120.0 * np.exp(np.cumsum(r))
        else:
            r = 0.8 * spy_rets + rng.normal(0, 0.006, n)
            data[tk] = 100.0 * np.exp(np.cumsum(r))

    vix_base = np.where(states == 2, 28.5, np.where(states == 1, 17.5, 13.2))
    data["^VIX"] = np.clip(vix_base + rng.normal(0, 1.8, n), 10.5, 65.0)

    df = pd.DataFrame(data, index=dates)
    return df, True


@st.cache_data(ttl=3600, show_spinner=False)
def load_multi_asset_data(tickers, start_date, end_date=None, force_demo=False):
    today = datetime.date.today()
    if isinstance(start_date, datetime.datetime):
        start_date = start_date.date()
    start_date = min(start_date, today - datetime.timedelta(days=90))
    fetch_start = start_date - datetime.timedelta(days=400)

    if end_date is None:
        end_dt = today
    else:
        end_dt = min(end_date, today)

    all_symbols = list(dict.fromkeys(list(tickers) + ["SPY", "^VIX"]))

    if force_demo:
        return _generate_markov_fallback(all_symbols, fetch_start, end_dt)

    try:
        yf_end = end_dt + datetime.timedelta(days=1)
        raw = yf.download(
            all_symbols,
            start=fetch_start.strftime("%Y-%m-%d"),
            end=yf_end.strftime("%Y-%m-%d"),
            auto_adjust=True,
            progress=False
        )
        if raw is None or raw.empty:
            return _generate_markov_fallback(all_symbols, fetch_start, end_dt)

        if isinstance(raw.columns, pd.MultiIndex):
            if "Close" in raw.columns.get_level_values(0):
                df = raw["Close"].copy()
            else:
                df = raw.xs(raw.columns.levels[0][0], axis=1, level=0).copy()
        else:
            df = raw.copy()

        df.index = pd.to_datetime(df.index).tz_localize(None)
        df = df[df.index.date <= today]
        df = df.ffill().bfill()

        if "SPY" not in df.columns or df["SPY"].isna().all() or len(df) < 260:
            return _generate_markov_fallback(all_symbols, fetch_start, end_dt)

        if "^VIX" not in df.columns or df["^VIX"].isna().all():
            df["^VIX"] = df["SPY"].pct_change().rolling(20).std() * np.sqrt(252) * 100
            df["^VIX"] = df["^VIX"].bfill().fillna(16.0)

        return df, False
    except Exception:
        return _generate_markov_fallback(all_symbols, fetch_start, end_dt)


# =====================================================================
# 2. FEATURE ENGINEERING & LABELLISATION SANS BIAIS
# =====================================================================

def build_features_and_targets(df_prices, target_horizon=20, bull_thresh=0.015, bear_thresh=-0.02):
    spy = df_prices["SPY"].copy()
    vix = df_prices["^VIX"].copy() if "^VIX" in df_prices.columns else spy.pct_change().rolling(20).std() * np.sqrt(252) * 100

    feat = pd.DataFrame(index=df_prices.index)
    log_ret = np.log(spy / spy.shift(1))

    feat["Ret_5d"] = np.log(spy / spy.shift(5))
    feat["Ret_20d"] = np.log(spy / spy.shift(20))
    feat["Ret_60d"] = np.log(spy / spy.shift(60))

    sma50 = spy.rolling(50).mean()
    sma200 = spy.rolling(200).mean()
    feat["Dist_SMA50"] = (spy - sma50) / sma50
    feat["Dist_SMA200"] = (spy - sma200) / sma200
    feat["Ratio_SMA50_200"] = sma50 / sma200 - 1.0

    vol20 = log_ret.rolling(20).std() * np.sqrt(252)
    vol60 = log_ret.rolling(60).std() * np.sqrt(252)
    feat["Vol_20d"] = vol20
    feat["Ratio_Vol20_60"] = (vol20 / vol60.replace(0, np.nan)).fillna(1.0)

    # RSI 14 séances
    delta = spy.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, 1e-9)
    feat["RSI_14"] = 100.0 - (100.0 / (1.0 + rs))

    feat["VIX_Level"] = vix
    feat["VIX_Stretch"] = vix / vix.rolling(20).mean().replace(0, 1.0) - 1.0

    features_clean = feat.dropna().copy()

    # Construction de la cible supervisée (Rendement forward 20j + Max Drawdown forward 20j)
    fwd_ret = spy.shift(-target_horizon) / spy - 1.0
    fwd_dd = pd.Series(index=spy.index, dtype=float)
    spy_vals = spy.values
    n = len(spy_vals)
    for i in range(n - target_horizon):
        window = spy_vals[i: i + target_horizon + 1]
        peaks = np.maximum.accumulate(window)
        dds = (window - peaks) / peaks
        fwd_dd.iloc[i] = np.min(dds)

    labels = pd.Series(1, index=spy.index, dtype=int)
    cond_bear = (fwd_ret < bear_thresh) | (fwd_dd < -0.05)
    cond_bull = (~cond_bear) & (fwd_ret > bull_thresh) & (fwd_dd > -0.03)
    labels[cond_bear] = 2
    labels[cond_bull] = 0

    dataset_train = features_clean.copy()
    dataset_train["Target"] = labels.reindex(features_clean.index)
    dataset_train["Fwd_Valid"] = fwd_ret.reindex(features_clean.index)
    dataset_train = dataset_train.dropna(subset=["Fwd_Valid"]).drop(columns=["Fwd_Valid"])
    dataset_train["Target"] = dataset_train["Target"].astype(int)

    return features_clean, dataset_train


# =====================================================================
# 3. MODÈLE ML WALK-FORWARD AVEC PURGING, EMBARGO & LIVE TAIL INFERENCE
# =====================================================================

class WalkForwardRegimeDetector:
    def __init__(self, model_type="rf", horizon=20, embargo=5):
        self.model_type = model_type
        self.horizon = horizon
        self.embargo = embargo

    def _build_estimator(self):
        if self.model_type == "xgb" and HAS_XGB:
            return XGBClassifier(
                n_estimators=90, max_depth=3, learning_rate=0.05,
                subsample=0.8, colsample_bytree=0.8, eval_metric="mlogloss", random_state=42
            )
        elif self.model_type == "cat" and HAS_CAT:
            return CatBoostClassifier(
                iterations=100, depth=4, learning_rate=0.05, verbose=0, random_seed=42
            )
        elif self.model_type == "logreg":
            return LogisticRegression(C=0.8, max_iter=500, class_weight="balanced", random_state=42)
        elif self.model_type in ["xgb", "cat"]:
            return HistGradientBoostingClassifier(max_depth=4, max_iter=90, random_state=42)
        else:
            return RandomForestClassifier(
                n_estimators=100, max_depth=4, class_weight="balanced_subsample", random_state=42
            )

    @staticmethod
    def _align_proba(model, X_scaled):
        raw_p = model.predict_proba(X_scaled)
        aligned = np.zeros((len(X_scaled), 3))
        for idx, cls in enumerate(model.classes_):
            if cls in [0, 1, 2]:
                aligned[:, int(cls)] = raw_p[:, idx]
        row_sums = aligned.sum(axis=1, keepdims=True)
        aligned = np.divide(aligned, np.where(row_sums == 0, 1.0, row_sums))
        return aligned

    def run_walk_forward(self, dataset_train, all_features, train_window=252, test_step=21):
        feat_cols = [c for c in all_features.columns if c != "Target"]
        n_train = len(dataset_train)
        purge_gap = self.horizon + self.embargo
        eff_window = min(train_window, max(60, int(n_train * 0.4)))

        preds = pd.Series(index=all_features.index, dtype=float)
        probs = pd.DataFrame(np.nan, index=all_features.index, columns=["P0", "P1", "P2"])
        importances = np.zeros(len(feat_cols))
        last_model = None
        last_scaler = None

        start_idx = eff_window + purge_gap
        for idx in range(start_idx, n_train, test_step):
            train_end = idx - purge_gap
            train_start = max(0, train_end - eff_window)
            train_slice = dataset_train.iloc[train_start:train_end]
            test_slice = dataset_train.iloc[idx: min(idx + test_step, n_train)]

            if len(train_slice) < 30 or len(test_slice) == 0:
                continue

            X_tr = train_slice[feat_cols].values
            y_tr = train_slice["Target"].values
            X_te = test_slice[feat_cols].values

            scaler = StandardScaler()
            X_tr_s = scaler.fit_transform(X_tr)
            X_te_s = scaler.transform(X_te)

            if len(np.unique(y_tr)) < 2:
                continue

            model = self._build_estimator()
            model.fit(X_tr_s, y_tr)
            p_mat = self._align_proba(model, X_te_s)

            probs.loc[test_slice.index, ["P0", "P1", "P2"]] = p_mat
            preds.loc[test_slice.index] = np.argmax(p_mat, axis=1)

            if hasattr(model, "feature_importances_"):
                importances = model.feature_importances_
            elif hasattr(model, "coef_"):
                importances = np.mean(np.abs(model.coef_), axis=0)

            last_model = model
            last_scaler = scaler

        # Entraînement final et Live Tail Inference sur les 25 derniers jours + début d'historique
        if last_model is None:
            scaler = StandardScaler()
            X_all_tr = scaler.fit_transform(dataset_train[feat_cols].values)
            y_all_tr = dataset_train["Target"].values
            last_model = self._build_estimator()
            last_model.fit(X_all_tr, y_all_tr)
            last_scaler = scaler
            if hasattr(last_model, "feature_importances_"):
                importances = last_model.feature_importances_

        missing_mask = preds.isna()
        if missing_mask.any():
            X_miss = last_scaler.transform(all_features.loc[missing_mask, feat_cols].values)
            p_miss = self._align_proba(last_model, X_miss)
            probs.loc[missing_mask, ["P0", "P1", "P2"]] = p_miss
            preds.loc[missing_mask] = np.argmax(p_miss, axis=1)

        # Précision Out-of-Sample sur les dates évaluées
        valid_eval = dataset_train.index.intersection(preds.dropna().index)
        oos_acc = float((preds.loc[valid_eval] == dataset_train.loc[valid_eval, "Target"]).mean())

        imp_sum = importances.sum()
        if imp_sum > 0:
            importances = importances / imp_sum
        else:
            importances = np.ones(len(feat_cols)) / len(feat_cols)

        feat_imp = pd.Series(importances, index=feat_cols).sort_values(ascending=True)
        return preds.astype(int), probs, feat_imp, oos_acc


# =====================================================================
# 4. OPTIMISATION DE MARKOWITZ (LEDOIT-WOLF + SLSQP)
# =====================================================================

def ledoit_wolf_covariance(returns):
    lw = LedoitWolf()
    lw.fit(returns.dropna().values)
    return pd.DataFrame(lw.covariance_ * 252.0, index=returns.columns, columns=returns.columns)


def optimize_portfolio(returns, max_weight=0.35, risk_free_rate=0.03):
    cols = list(returns.columns)
    n = len(cols)
    eff_max = max(max_weight, 1.0 / n + 0.02)

    mu = returns.mean().values * 252.0
    cov = ledoit_wolf_covariance(returns).values

    def neg_sharpe(w):
        port_ret = np.dot(w, mu)
        port_vol = np.sqrt(max(np.dot(w.T, np.dot(cov, w)), 1e-8))
        return -(port_ret - risk_free_rate) / port_vol

    w0 = np.ones(n) / n
    bounds = tuple((0.0, eff_max) for _ in range(n))
    cons = ({"type": "eq", "fun": lambda w: np.sum(w) - 1.0},)

    res = minimize(neg_sharpe, w0, method="SLSQP", bounds=bounds, constraints=cons)
    weights = res.x if res.success else w0
    weights = np.clip(weights, 0, None)
    weights /= weights.sum()
    return pd.Series(weights, index=cols)


def compute_dynamic_regime_allocation(regime, base_weights, defensive_assets=("GLD", "TLT", "SHY")):
    w = base_weights.copy()
    def_cols = [c for c in w.index if c in defensive_assets]
    eq_cols = [c for c in w.index if c not in defensive_assets]

    if not def_cols or not eq_cols:
        return w

    target_eq = {0: 0.90, 1: 0.65, 2: 0.15}.get(int(regime), 0.65)
    target_def = 1.0 - target_eq

    eq_sum = w[eq_cols].sum()
    def_sum = w[def_cols].sum()

    if eq_sum > 0:
        w[eq_cols] = w[eq_cols] / eq_sum * target_eq
    else:
        w[eq_cols] = target_eq / len(eq_cols)

    if def_sum > 0:
        w[def_cols] = w[def_cols] / def_sum * target_def
    else:
        w[def_cols] = target_def / len(def_cols)

    return w / w.sum()


# =====================================================================
# 5. COUVERTURE EN OPTIONS BLACK-SCHOLES (1973) & GRECQUES
# =====================================================================

class BlackScholesEngine:
    @staticmethod
    def _d1_d2(S, K, T, r, sigma):
        T = max(T, 1e-5)
        sigma = max(sigma, 0.05)
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return d1, d2

    @classmethod
    def put_price(cls, S, K, T, r, sigma):
        d1, d2 = cls._d1_d2(S, K, T, r, sigma)
        return float(K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1))

    @classmethod
    def compute_greeks(cls, S, K, T, r, sigma):
        T = max(T, 1e-4)
        sigma = max(sigma, 0.05)
        d1, d2 = cls._d1_d2(S, K, T, r, sigma)
        pdf_d1 = norm.pdf(d1)

        delta = norm.cdf(d1) - 1.0
        gamma = pdf_d1 / (S * sigma * np.sqrt(T))
        theta_annual = -(S * pdf_d1 * sigma) / (2.0 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)
        theta_daily = theta_annual / 365.0
        vega_pct = S * pdf_d1 * np.sqrt(T) * 0.01

        return {
            "Delta": float(delta),
            "Gamma": float(gamma),
            "Theta": float(theta_daily),
            "Vega": float(vega_pct),
            "Put_Price": cls.put_price(S, K, T, r, sigma)
        }


def simulate_options_hedged_portfolio(spot_series, vix_series, regime_series, hedge_otm_pct=0.05, r=0.03):
    dates = spot_series.index
    spot = spot_series.values
    vix = (vix_series.reindex(dates).ffill().bfill().values) / 100.0
    regimes = regime_series.reindex(dates).fillna(1).values

    unhedged = 100.0 * (spot / spot[0])
    hedged = np.zeros(len(dates))
    hedged[0] = 100.0

    active_put = False
    K = 0.0
    days_left = 0
    prev_put_val = 0.0
    units = 0.0

    for i in range(1, len(dates)):
        s_prev, s_curr = spot[i - 1], spot[i]
        sig = max(vix[i], 0.10)
        base_ret = (s_curr / s_prev) - 1.0
        port_val = hedged[i - 1] * (1.0 + base_ret)

        if active_put:
            days_left -= 1
            T_rem = max(days_left / 252.0, 1e-5)
            curr_put_val = BlackScholesEngine.put_price(s_curr, K, T_rem, r, sig)
            pnl_put = units * (curr_put_val - prev_put_val)
            port_val += pnl_put
            prev_put_val = curr_put_val
            if days_left <= 0 or regimes[i] != 2:
                active_put = False

        if (not active_put) and regimes[i] == 2:
            active_put = True
            days_left = 21
            K = s_curr * (1.0 - hedge_otm_pct)
            T_init = days_left / 252.0
            prev_put_val = BlackScholesEngine.put_price(s_curr, K, T_init, r, sig)
            units = port_val / s_curr
            # Coût d'entrée lissé de la prime
            port_val -= units * prev_put_val * 0.15

        hedged[i] = port_val

    return pd.DataFrame({"Unhedged_SPY": unhedged, "Put_Hedged_Portfolio": hedged}, index=dates)


# =====================================================================
# 6. BACKTESTER INSTITUTIONNEL & MÉTRIQUES DE PERFORMANCE
# =====================================================================

def compute_financial_metrics(wealth_series, risk_free_rate=0.03):
    rets = wealth_series.pct_change().dropna()
    if len(rets) < 5:
        return {k: 0.0 for k in ["Total Return", "CAGR", "Ann. Volatility", "Sharpe Ratio", "Sortino Ratio", "Max Drawdown", "Calmar Ratio"]}

    total_ret = (wealth_series.iloc[-1] / wealth_series.iloc[0]) - 1.0
    n_years = max(len(rets) / 252.0, 0.1)
    cagr = (wealth_series.iloc[-1] / wealth_series.iloc[0]) ** (1.0 / n_years) - 1.0
    vol = rets.std() * np.sqrt(252.0)
    sharpe = (cagr - risk_free_rate) / vol if vol > 0 else 0.0

    downside = rets[rets < 0].std() * np.sqrt(252.0)
    sortino = (cagr - risk_free_rate) / downside if downside > 0 else 0.0

    peaks = wealth_series.cummax()
    dd = (wealth_series - peaks) / peaks
    max_dd = float(dd.min())
    calmar = cagr / abs(max_dd) if max_dd < 0 else 0.0

    return {
        "Total Return": total_ret * 100,
        "CAGR": cagr * 100,
        "Ann. Volatility": vol * 100,
        "Sharpe Ratio": sharpe,
        "Sortino Ratio": sortino,
        "Max Drawdown": max_dd * 100,
        "Calmar Ratio": calmar,
    }


def run_strategy_backtest(df_prices, regime_series, base_weights, fee_bps=10, slip_bps=5):
    assets = list(base_weights.index)
    rets = df_prices[assets].pct_change().fillna(0.0)
    regimes = regime_series.reindex(df_prices.index).ffill().bfill().fillna(1)

    total_cost_rate = (fee_bps + slip_bps) / 10000.0
    w_map = {
        r: compute_dynamic_regime_allocation(r, base_weights).values
        for r in [0, 1, 2]
    }

    n = len(df_prices)
    strat_rets = np.zeros(n)
    prev_w = w_map[int(regimes.iloc[0])]

    for i in range(1, n):
        r_prev = int(regimes.iloc[i - 1])
        target_w = w_map[r_prev]
        turnover = np.sum(np.abs(target_w - prev_w))
        friction = turnover * total_cost_rate
        day_ret = np.dot(target_w, rets.iloc[i].values) - friction
        strat_rets[i] = day_ret
        prev_w = target_w

    wealth_strat = 100.0 * np.cumprod(1.0 + strat_rets)
    wealth_spy = 100.0 * (df_prices["SPY"] / df_prices["SPY"].iloc[0])

    bond_col = "TLT" if "TLT" in df_prices.columns else ("SHY" if "SHY" in df_prices.columns else "SPY")
    ret_60_40 = 0.60 * df_prices["SPY"].pct_change().fillna(0.0) + 0.40 * df_prices[bond_col].pct_change().fillna(0.0)
    wealth_60_40 = 100.0 * np.cumprod(1.0 + ret_60_40.values)

    bt_df = pd.DataFrame({
        "Dynamic Quant Engine": wealth_strat,
        "Benchmark 60/40": wealth_60_40,
        "S&P 500 Buy & Hold": wealth_spy.values
    }, index=df_prices.index)

    metrics_df = pd.DataFrame({
        col: compute_financial_metrics(bt_df[col]) for col in bt_df.columns
    }).T

    return bt_df, metrics_df


# =====================================================================
# 7. PIPELINE MAÎTRE D'EXÉCUTION (POINT D'ENTRÉE UNIQUE POUR APP.PY)
# =====================================================================

def run_full_quant_pipeline(tickers, start_date, model_key, max_weight, fee_bps, slip_bps, force_demo):
    df_all, is_demo = load_multi_asset_data(tickers, start_date=start_date, force_demo=force_demo)
    features_clean, dataset_train = build_features_and_targets(df_all)

    detector = WalkForwardRegimeDetector(model_type=model_key, horizon=20, embargo=5)
    preds, probs, feat_imp, oos_acc = detector.run_walk_forward(dataset_train, features_clean)

    # Filtrage à partir de la date choisie par l'utilisateur (après le Warm-up Buffer de 400j)
    user_ts = pd.Timestamp(start_date)
    df_view = df_all[df_all.index >= user_ts].copy()
    if len(df_view) < 30:
        df_view = df_all.iloc[-120:].copy()

    preds_view = preds.reindex(df_view.index).ffill().bfill().fillna(1).astype(int)
    probs_view = probs.reindex(df_view.index).ffill().bfill().fillna(0.33)

    valid_assets = [t for t in tickers if t in df_view.columns and t != "^VIX"]
    if not valid_assets:
        valid_assets = ["SPY"]

    asset_returns = df_view[valid_assets].pct_change().dropna()
    static_weights = optimize_portfolio(asset_returns, max_weight=max_weight)
    current_regime = int(preds_view.iloc[-1])
    dynamic_weights = compute_dynamic_regime_allocation(current_regime, static_weights)

    bt_df, metrics_df = run_strategy_backtest(
        df_view, preds_view, static_weights, fee_bps=fee_bps, slip_bps=slip_bps
    )

    spot_spy = df_view["SPY"]
    vix_ser = df_view["^VIX"]
    options_df = simulate_options_hedged_portfolio(spot_spy, vix_ser, preds_view)

    last_spot = float(spot_spy.iloc[-1])
    last_vix = float(vix_ser.iloc[-1])
    greeks = BlackScholesEngine.compute_greeks(
        S=last_spot, K=last_spot * 0.95, T=30.0 / 365.0, r=0.03, sigma=last_vix / 100.0
    )

    return {
        "is_demo": is_demo,
        "df_view": df_view,
        "preds": preds_view,
        "probs": probs_view,
        "feat_imp": feat_imp,
        "oos_acc": oos_acc,
        "current_regime": current_regime,
        "last_probs": probs_view.iloc[-1],
        "last_spot": last_spot,
        "last_vix": last_vix,
        "static_weights": static_weights,
        "dynamic_weights": dynamic_weights,
        "bt_df": bt_df,
        "metrics_df": metrics_df,
        "options_df": options_df,
        "greeks": greeks,
        "last_date": df_view.index[-1].strftime("%Y-%m-%d")
    }