# app.py

import os
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- AUTO-GÉNÉRATION DE LA CONFIGURATION STREAMLIT SOMBRE ---
os.makedirs(".streamlit", exist_ok=True)
_cfg_file = os.path.join(".streamlit", "config.toml")
if not os.path.exists(_cfg_file):
    with open(_cfg_file, "w", encoding="utf-8") as _f:
        _f.write(
            '[theme]\n'
            'base = "dark"\n'
            'backgroundColor = "#050506"\n'
            'secondaryBackgroundColor = "#0D0D0F"\n'
            'primaryColor = "#10B981"\n'
            'textColor = "#E6EDF3"\n'
            'font = "sans serif"\n\n'
            '[server]\n'
            'headless = true\n'
        )

import streamlit as st
import streamlit.components.v1 as components

from i18n import I18N
from backend import run_full_quant_pipeline

st.set_page_config(
    page_title="QUANTITATIVE REGIME & PORTFOLIO ENGINE",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "view" not in st.session_state:
    st.session_state["view"] = "landing"
if "lang" not in st.session_state:
    st.session_state["lang"] = "FR"


# =====================================================================
# 1. INJECTION DU DESIGN SYSTEM (TOTAL MATTE BLACK & BENTO GLASSMORPHISM)
# =====================================================================

def inject_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        html, body, [class*="css"], .stApp {
            background-color: #050506 !important;
            color: #E6EDF3 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
        }
        .block-container {
            padding-top: 1.6rem !important;
            padding-bottom: 2rem !important;
            max-width: 1440px !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #08080A !important;
            border-right: 1px solid #1F1F24 !important;
        }

        /* Hero Styling */
        .hero-title {
            font-size: 3.1rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.08;
            color: #FFFFFF;
            margin-bottom: 0.75rem;
            text-transform: uppercase;
        }
        .hero-subtitle {
            font-size: 1.15rem;
            font-weight: 400;
            color: #9CA3AF;
            margin-bottom: 1rem;
            line-height: 1.5;
        }
        .hero-mono-badge {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            letter-spacing: 0.08em;
            color: #A1A1AA;
            padding: 6px 12px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid #1F1F24;
            border-radius: 6px;
            display: inline-block;
            margin-bottom: 1rem;
        }

        /* Bento KPI Cards */
        .bento-card {
            background: rgba(13, 13, 15, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 18px 20px;
            height: 138px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.2s ease;
        }
        .bento-cyan {
            border-top: 2px solid #06B6D4;
            box-shadow: inset 0 18px 28px -18px rgba(6, 182, 212, 0.35), 0 0 20px rgba(6, 182, 212, 0.08);
        }
        .bento-green {
            border-top: 2px solid #10B981;
            box-shadow: inset 0 18px 28px -18px rgba(16, 185, 129, 0.35), 0 0 20px rgba(16, 185, 129, 0.08);
        }
        .bento-amber {
            border-top: 2px solid #F59E0B;
            box-shadow: inset 0 18px 28px -18px rgba(245, 158, 11, 0.35), 0 0 20px rgba(245, 158, 11, 0.08);
        }
        .bento-red {
            border-top: 2px solid #EF4444;
            box-shadow: inset 0 18px 28px -18px rgba(239, 68, 68, 0.42), 0 0 22px rgba(239, 68, 68, 0.12);
        }
        .kpi-label {
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            color: #A1A1AA;
            text-transform: uppercase;
        }
        .kpi-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.65rem;
            font-weight: 700;
            line-height: 1.15;
            margin: 4px 0;
        }
        .kpi-sub {
            font-size: 0.76rem;
            color: #9CA3AF;
        }

        /* Chart & Section Containers */
        .panel-box {
            background: #0D0D0F;
            border: 1px solid #1F1F24;
            border-radius: 12px;
            padding: 16px 20px;
            margin-top: 12px;
        }

        /* Live Stats Bar on Landing */
        .live-stats-bar {
            background: rgba(13, 13, 15, 0.75);
            border: 1px solid #1F1F24;
            border-radius: 10px;
            padding: 14px 22px;
            margin: 10px 0 18px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.88rem;
        }

        /* Buttons */
        div.stButton > button {
            background: #121318 !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 8px !important;
            padding: 0.72rem 1.4rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.04em !important;
            width: 100% !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button:hover {
            border-color: #10B981 !important;
            box-shadow: 0 0 18px rgba(16, 185, 129, 0.25) !important;
            background: #161820 !important;
        }

        /* Tabs styling */
        button[data-baseweb="tab"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.84rem !important;
            color: #9CA3AF !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #10B981 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# =====================================================================
# 2. COMPOSANT WEBGL / CANVAS 3D : LE GLOBE MACROÉCONOMIQUE INTERACTIF
# =====================================================================

def render_interactive_3d_globe():
    globe_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {
            margin: 0;
            background: #050506;
            overflow: hidden;
            font-family: 'Inter', -apple-system, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 440px;
        }
        #globe-wrapper {
            position: relative;
            width: 100%;
            height: 440px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        canvas {
            cursor: grab;
        }
        canvas:active {
            cursor: grabbing;
        }
        .flash-card {
            position: absolute;
            top: 42px;
            right: 28px;
            width: 310px;
            background: rgba(13, 13, 17, 0.86);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 10px;
            padding: 13px 15px;
            color: #E6EDF3;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.75);
            pointer-events: none;
            transition: all 0.25s ease;
        }
        .flash-header {
            font-family: 'JetBrains Mono', monospace;
            font-size: 10.5px;
            font-weight: 700;
            color: #E6EDF3;
            letter-spacing: 0.04em;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            padding-bottom: 6px;
            margin-bottom: 8px;
        }
        .flash-body {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }
        .flash-metrics {
            font-family: 'JetBrains Mono', monospace;
            font-size: 10.5px;
            line-height: 1.55;
            width: 54%;
        }
        .m-row {
            display: flex;
            justify-content: space-between;
        }
        .c-green { color: #10B981; }
        .c-red { color: #EF4444; }
        .c-amber { color: #F59E0B; }
        .flash-desc {
            margin-top: 7px;
            font-size: 10.5px;
            color: #9CA3AF;
            line-height: 1.35;
        }
    </style>
    </head>
    <body>
    <div id="globe-wrapper">
        <canvas id="globeCanvas" width="680" height="440"></canvas>
        <div class="flash-card" id="flashCard">
            <div class="flash-header" id="flashTitle">FLASH INFO // US Market - Inflation Data Impact</div>
            <div class="flash-body">
                <svg width="120" height="58" viewBox="0 0 120 58">
                    <defs>
                        <linearGradient id="sparkGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stop-color="#10B981" stop-opacity="0.45"/>
                            <stop offset="100%" stop-color="#10B981" stop-opacity="0.0"/>
                        </linearGradient>
                    </defs>
                    <path id="sparkArea" d="M2,48 L18,40 L34,43 L50,26 L66,30 L82,16 L98,22 L116,8 L116,56 L2,56 Z" fill="url(#sparkGrad)"/>
                    <path id="sparkLine" d="M2,48 L18,40 L34,43 L50,26 L66,30 L82,16 L98,22 L116,8" fill="none" stroke="#10B981" stroke-width="2"/>
                </svg>
                <div class="flash-metrics">
                    <div class="m-row"><span>• 15.55%</span><span class="c-green">158.85B</span></div>
                    <div class="m-row"><span>• 33.77%</span><span class="c-green">+33.59B</span></div>
                    <div class="m-row"><span>• 29.23%</span><span class="c-red">+35.93B</span></div>
                    <div class="m-row"><span>• 94.23%</span><span class="c-red">+37.92B</span></div>
                </div>
            </div>
            <div class="flash-desc" id="flashDesc">
                Anticipation Fed & flux macro US — Bascule de probabilité vers couverture Put OTM.
            </div>
        </div>
    </div>

    <script>
    const canvas = document.getElementById('globeCanvas');
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    const cx = W * 0.40, cy = H * 0.52, R = 158;

    let rotY = -0.6;
    let rotX = 0.25;
    let isDragging = false, prevX = 0, prevY = 0;

    const dots = [];
    for (let lat = -75; lat <= 75; lat += 4.5) {
        const rLat = (lat * Math.PI) / 180;
        const stepLon = 4.5 / Math.max(0.25, Math.cos(rLat));
        for (let lon = -180; lon < 180; lon += stepLon) {
            const isLand = (
                (lat > 15 && lat < 65 && lon > -130 && lon < -60) ||
                (lat > -50 && lat < 12 && lon > -80 && lon < -35) ||
                (lat > 35 && lat < 68 && lon > -10 && lon < 45) ||
                (lat > -32 && lat < 32 && lon > -18 && lon < 48) ||
                (lat > 10 && lat < 65 && lon > 45 && lon < 145) ||
                (lat > -38 && lat < -12 && lon > 112 && lon < 152)
            );
            dots.push({
                lat: rLat,
                lon: (lon * Math.PI) / 180,
                land: isLand
            });
        }
    }

    const hotspots = [
        {
            lat: 0.66, lon: -1.35, size: 8,
            title: "FLASH INFO // US Market - Inflation Data Impact",
            desc: "BANQUE CENTRALE & POLITIQUE // Tensions taux Fed & tarifs douaniers — Alerte Régime R2."
        },
        {
            lat: 0.78, lon: -1.75, size: 6.5,
            title: "FLASH INFO // Silicon Valley - Tech Liquidity Flow",
            desc: "SECTEUR TECH // Rotation factorielle QQQ/SPY & hausse de la volatilité implicite VIX."
        },
        {
            lat: 0.85, lon: 0.15, size: 7,
            title: "FLASH INFO // Eurozone - ECB Monetary Feed",
            desc: "MACRO EUROPE // Compression de croissance industrielle EZU/VGK — Surpondération Or (GLD)."
        },
        {
            lat: 0.42, lon: 2.12, size: 8,
            title: "FLASH INFO // Taiwan Strait - Semiconductor Supply",
            desc: "SEMI-CONDUCTEURS // Tensions chaîne d'approvisionnement TSMC — Volatilité Tech : ÉLEVÉE."
        },
        {
            lat: 0.48, lon: 0.78, size: 7,
            title: "FLASH INFO // Middle East - Energy & Commodity Shock",
            desc: "GÉOPOLITIQUE // Choc énergétique & prime de risque géostratégique — Couverture Put OTM active."
        },
        {
            lat: -0.38, lon: -0.82, size: 6.5,
            title: "FLASH INFO // EM Commodities - Brazil & LatAm Desk",
            desc: "MATIÈRES PREMIÈRES // Flux de capitaux émergents & arbitrage de courbe obligataire."
        }
    ];

    canvas.addEventListener('mousedown', e => { isDragging = true; prevX = e.clientX; prevY = e.clientY; });
    window.addEventListener('mouseup', () => { isDragging = false; });
    window.addEventListener('mousemove', e => {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;

        if (isDragging) {
            rotY += (e.clientX - prevX) * 0.008;
            rotX = Math.max(-0.8, Math.min(0.8, rotX + (e.clientY - prevY) * 0.008));
            prevX = e.clientX; prevY = e.clientY;
        }

        for (const h of hotspots) {
            if (h.screenZ > 0 && Math.hypot(mx - h.screenX, my - h.screenY) < 18) {
                document.getElementById('flashTitle').innerText = h.title;
                document.getElementById('flashDesc').innerText = h.desc;
                break;
            }
        }
    });

    let pulse = 0;
    function project(lat, lon, radius) {
        const x0 = radius * Math.cos(lat) * Math.sin(lon + rotY);
        const y0 = radius * Math.sin(lat);
        const z0 = radius * Math.cos(lat) * Math.cos(lon + rotY);

        const y1 = y0 * Math.cos(rotX) - z0 * Math.sin(rotX);
        const z1 = y0 * Math.sin(rotX) + z0 * Math.cos(rotX);
        return { x: cx + x0, y: cy - y1, z: z1 };
    }

    function draw() {
        ctx.clearRect(0, 0, W, H);
        if (!isDragging) rotY += 0.0032;
        pulse += 0.06;

        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(-0.32);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.11)";
        ctx.setLineDash([3, 6]);
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.ellipse(0, 0, R + 34, R + 12, 0, 0, Math.PI * 2);
        ctx.stroke();

        ctx.rotate(0.64);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.07)";
        ctx.beginPath();
        ctx.ellipse(0, 0, R + 22, R + 38, 0, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();

        const grad = ctx.createRadialGradient(cx - 40, cy - 40, R * 0.1, cx, cy, R);
        grad.addColorStop(0, "#1A1B20");
        grad.addColorStop(0.85, "#09090C");
        grad.addColorStop(1, "#040405");
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(cx, cy, R, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = "rgba(255, 255, 255, 0.18)";
        ctx.lineWidth = 1.1;
        ctx.stroke();

        for (const d of dots) {
            const p = project(d.lat, d.lon, R);
            if (p.z > 0) {
                const alpha = (p.z / R) * (d.land ? 0.68 : 0.14);
                ctx.fillStyle = d.land
                    ? `rgba(220, 225, 235, ${alpha.toFixed(2)})`
                    : `rgba(130, 140, 155, ${alpha.toFixed(2)})`;
                const sz = d.land ? 1.55 : 1.0;
                ctx.fillRect(p.x, p.y, sz, sz);
            }
        }

        for (const h of hotspots) {
            const p = project(h.lat, h.lon, R);
            h.screenX = p.x;
            h.screenY = p.y;
            h.screenZ = p.z;

            if (p.z > -15) {
                const glowRadius = h.size * (2.6 + 0.5 * Math.sin(pulse));
                const g = ctx.createRadialGradient(p.x, p.y, 1, p.x, p.y, glowRadius);
                g.addColorStop(0, "rgba(239, 68, 68, 0.95)");
                g.addColorStop(0.4, "rgba(239, 68, 68, 0.38)");
                g.addColorStop(1, "rgba(239, 68, 68, 0)");

                ctx.fillStyle = g;
                ctx.beginPath();
                ctx.arc(p.x, p.y, glowRadius, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = "#FCA5A5";
                ctx.beginPath();
                ctx.arc(p.x, p.y, 3.2, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        requestAnimationFrame(draw);
    }
    draw();
    </script>
    </body>
    </html>
    """
    components.html(globe_html, height=445)


# =====================================================================
# 3. GRAPHIQUES PLOTLY HAUTE PRÉCISION (COURBE TRICOLORE + HALO)
# =====================================================================

def build_regime_glow_chart(df_view, preds, title):
    fig = go.Figure()
    spy = df_view["SPY"]

    fig.add_trace(go.Scatter(
        x=df_view.index, y=spy,
        mode="lines",
        line=dict(color="rgba(255,255,255,0.18)", width=1),
        name="SPY Price",
        hoverinfo="skip"
    ))

    regime_cfg = [
        (0, "Bullish (R0)", "#10B981", "rgba(16, 185, 129, 0.12)"),
        (1, "Neutral (R1)", "#06B6D4", "rgba(6, 182, 212, 0.10)"),
        (2, "Sell-off (R2)", "#EF4444", "rgba(239, 68, 68, 0.16)"),
    ]

    for r_code, r_label, hex_col, fill_rgba in regime_cfg:
        mask = (preds == r_code) | (preds.shift(1) == r_code)
        y_masked = spy.where(mask, np.nan)

        fig.add_trace(go.Scatter(
            x=df_view.index,
            y=y_masked,
            mode="lines",
            name=r_label,
            line=dict(color=hex_col, width=2.4),
            fill="tozeroy",
            fillcolor=fill_rgba,
            hovertemplate=f"<b>{r_label}</b>: $%{{y:.2f}}<extra></extra>"
        ))

    y_min = float(spy.min()) * 0.95
    y_max = float(spy.max()) * 1.03

    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#FFFFFF")),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=390,
        margin=dict(l=10, r=10, t=42, b=10),
        hovermode="x unified",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            bgcolor="rgba(13,13,15,0.8)", bordercolor="#1F1F24", borderwidth=1
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", zeroline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", range=[y_min, y_max], zeroline=False)
    )
    return fig


# =====================================================================
# 4. VUE 1 : LANDING PAGE VITRINE HAUTE TECHNOLOGIE + APERÇU TERMINAL
# =====================================================================

def render_landing_page(t, results):
    col_left, col_right = st.columns([1.05, 1.15], gap="large")

    with col_left:
        st.markdown(f'<div class="hero-title">{t["hero_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-subtitle">{t["hero_sub"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-mono-badge">{t["hero_badge"]}</div>', unsafe_allow_html=True)

        render_interactive_3d_globe()

        st.markdown(
            f"""
            <div style="font-size:0.78rem; letter-spacing:0.08em; color:#9CA3AF; font-weight:600; margin-top:4px;">
                {t["stats_header"]}
            </div>
            <div class="live-stats-bar">
                <div><span style="color:#9CA3AF;">Volume Traité :</span> <b>$1.2B+</b></div>
                <div><span style="color:#9CA3AF;">Actifs Analysés :</span> <b>18+</b></div>
                <div><span style="color:#9CA3AF;">Précision Machine :</span> <b style="color:#10B981;">{results['oos_acc']*100:.1f}%</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(t["cta_enter"], key="btn_enter_terminal"):
            st.session_state["view"] = "terminal"
            st.rerun()

    with col_right:
        st.markdown(
            """
            <div style="background:#0A0A0D; border:1px solid #1F1F24; border-radius:14px; padding:18px 20px;">
                <div style="font-size:0.88rem; color:#9CA3AF; font-weight:600; border-bottom:1px solid #1F1F24; padding-bottom:10px; margin-bottom:14px;">
                    Terminal // Live Institutional Preview
                </div>
            """,
            unsafe_allow_html=True
        )
        render_kpi_row(t, results)
        fig_preview = build_regime_glow_chart(results["df_view"], results["preds"], t["chart_regime_title"])
        st.plotly_chart(fig_preview, use_container_width=True, key="landing_preview_chart")
        st.markdown("</div>", unsafe_allow_html=True)


# =====================================================================
# 5. CARTES KPI BENTO GRID & VUE 2 : LE TERMINAL QUANTITATIF COMPLET
# =====================================================================

def render_kpi_row(t, results):
    reg = results["current_regime"]
    p0 = float(results["last_probs"]["P0"]) * 100
    p2 = float(results["last_probs"]["P2"]) * 100
    vix = results["last_vix"]
    spot = results["last_spot"]

    reg_meta = {
        0: (t["regime_0_name"], t["regime_0_desc"], "bento-green", "#10B981"),
        1: (t["regime_1_name"], t["regime_1_desc"], "bento-cyan", "#06B6D4"),
        2: (t["regime_2_name"], t["regime_2_desc"], "bento-red", "#EF4444"),
    }[reg]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="bento-card {reg_meta[2]}">
                <div class="kpi-label">{t["kpi_1_title"]}</div>
                <div class="kpi-value" style="color:{reg_meta[3]}; font-size:1.30rem;">{reg_meta[0]}</div>
                <div class="kpi-sub">{reg_meta[1]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="bento-card bento-green">
                <div class="kpi-label">{t["kpi_2_title"]}</div>
                <div class="kpi-value" style="color:#10B981;">{p0:.1f}%</div>
                <div class="kpi-sub">Confidence Score: {"High" if p0 > 50 else "Moderate"}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        tail_status = "CRITICAL" if p2 > 45 else ("ELEVATED" if p2 > 25 else "CONTAINED")
        card_cls = "bento-red" if p2 > 45 else "bento-amber"
        val_col = "#EF4444" if p2 > 45 else "#F59E0B"
        st.markdown(
            f"""
            <div class="bento-card {card_cls}">
                <div class="kpi-label">{t["kpi_3_title"]}</div>
                <div class="kpi-value" style="color:{val_col};">{p2:.1f}%</div>
                <div class="kpi-sub">Tail-Risk Alert: <b style="color:{val_col};">{tail_status}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f"""
            <div class="bento-card bento-cyan">
                <div class="kpi-label">{t["kpi_4_title"]}</div>
                <div class="kpi-value" style="color:#38BDF8;">{vix:.2f}</div>
                <div class="kpi-sub">SPY Ref: <b>${spot:.2f}</b> • Sync: {results["last_date"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_terminal_view(t, results):
    top_l, top_r = st.columns([3.5, 1])
    with top_l:
        st.markdown(
            f"""
            <div style="background:#0D0D0F; border:1px solid #1F1F24; border-radius:8px; padding:10px 16px; font-size:0.78rem; color:#9CA3AF; margin-bottom:14px;">
                <span style="color:#10B981; font-family:'JetBrains Mono',monospace; font-weight:700;">LIVE DATA FEED • SYNCED ({results['last_date']})</span>
                &nbsp;|&nbsp; {t["legal_banner"]}
            </div>
            """,
            unsafe_allow_html=True
        )
    with top_r:
        if st.button(t["cta_back"], key="btn_back_landing"):
            st.session_state["view"] = "landing"
            st.rerun()

    render_kpi_row(t, results)
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    tabs = st.tabs([t["tab_1"], t["tab_2"], t["tab_3"], t["tab_4"], t["tab_5"]])

    with tabs[0]:
        col_main, col_imp = st.columns([1.85, 1])
        with col_main:
            fig_reg = build_regime_glow_chart(results["df_view"], results["preds"], t["chart_regime_title"])
            st.plotly_chart(fig_reg, use_container_width=True, key="term_main_regime_chart")
        with col_imp:
            imp = results["feat_imp"]
            fig_imp = go.Figure(go.Bar(
                x=imp.values * 100,
                y=imp.index,
                orientation="h",
                marker=dict(color="#06B6D4", line=dict(color="#10B981", width=1))
            ))
            fig_imp.update_layout(
                title=dict(text=t["chart_feat_title"], font=dict(size=14, color="#FFFFFF")),
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=390,
                margin=dict(l=10, r=10, t=42, b=10),
                xaxis=dict(title="Importance (%)", gridcolor="rgba(255,255,255,0.04)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.04)")
            )
            st.plotly_chart(fig_imp, use_container_width=True)

    with tabs[1]:
        c_p1, c_p2 = st.columns(2)
        palette = ["#10B981", "#06B6D4", "#3B82F6", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899"]
        with c_p1:
            sw = results["static_weights"]
            fig_s = go.Figure(go.Pie(
                labels=sw.index, values=sw.values, hole=0.58,
                marker=dict(colors=palette, line=dict(color="#050506", width=2))
            ))
            fig_s.update_layout(
                title=t["chart_alloc_static"], template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", height=360
            )
            st.plotly_chart(fig_s, use_container_width=True)
        with c_p2:
            dw = results["dynamic_weights"]
            fig_d = go.Figure(go.Pie(
                labels=dw.index, values=dw.values, hole=0.58,
                marker=dict(colors=palette, line=dict(color="#050506", width=2))
            ))
            fig_d.update_layout(
                title=t["chart_alloc_dyn"], template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", height=360
            )
            st.plotly_chart(fig_d, use_container_width=True)

    with tabs[2]:
        bt_df = results["bt_df"]
        fig_bt = go.Figure()
        colors_bt = {"Dynamic Quant Engine": "#10B981", "Benchmark 60/40": "#06B6D4", "S&P 500 Buy & Hold": "#9CA3AF"}
        for col in bt_df.columns:
            fig_bt.add_trace(go.Scatter(
                x=bt_df.index, y=bt_df[col], mode="lines", name=col,
                line=dict(color=colors_bt.get(col, "#FFFFFF"), width=2.4 if col == "Dynamic Quant Engine" else 1.6)
            ))
        fig_bt.update_layout(
            title=t["chart_bt_title"], template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=370, hovermode="x unified",
            xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)")
        )
        st.plotly_chart(fig_bt, use_container_width=True)
        st.dataframe(results["metrics_df"].style.format("{:.2f}"), use_container_width=True)

    with tabs[3]:
        g = results["greeks"]
        gc1, gc2, gc3, gc4 = st.columns(4)
        for col_ui, (k_name, k_val, k_col) in zip(
            [gc1, gc2, gc3, gc4],
            [("DELTA (Δ) PUT 5% OTM", f"{g['Delta']:.3f}", "#06B6D4"),
             ("GAMMA (Γ) CONVEXITÉ", f"{g['Gamma']:.4f}", "#10B981"),
             ("THÊTA (Θ) $/JOUR", f"{g['Theta']:.3f}", "#EF4444"),
             ("VEGA (ν) / 1% VOL", f"{g['Vega']:.3f}", "#F59E0B")]
        ):
            with col_ui:
                st.markdown(
                    f"""
                    <div class="bento-card" style="height:105px;">
                        <div class="kpi-label">{k_name}</div>
                        <div class="kpi-value" style="color:{k_col}; font-size:1.45rem;">{k_val}</div>
                        <div class="kpi-sub">Prime Put 30j Estimée : ${g['Put_Price']:.2f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        opt_df = results["options_df"]
        fig_opt = go.Figure()
        fig_opt.add_trace(go.Scatter(
            x=opt_df.index, y=opt_df["Put_Hedged_Portfolio"],
            mode="lines", name="Put Hedged Portfolio (Active on R2)",
            line=dict(color="#10B981", width=2.4)
        ))
        fig_opt.add_trace(go.Scatter(
            x=opt_df.index, y=opt_df["Unhedged_SPY"],
            mode="lines", name="Unhedged Equity (SPY)",
            line=dict(color="#EF4444", width=1.6, dash="dot")
        ))
        fig_opt.update_layout(
            title=t["chart_opt_title"], template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=360, hovermode="x unified"
        )
        st.plotly_chart(fig_opt, use_container_width=True)

    with tabs[4]:
        st.markdown(
            """
            <div class="panel-box" style="line-height:1.7;">
                <h4 style="color:#10B981; margin-top:0;">Architecture Quantitative & Garantie Zéro Look-Ahead Bias</h4>
                <ul>
                    <li><b>Classification des Régimes vs Prédiction Naïve :</b> Le rapport signal/bruit des rendements quotidiens étant proche de zéro, le moteur classifie la distribution conditionnelle à 20 jours en 3 régimes (<i>R0 Bullish</i>, <i>R1 Ranging</i>, <i>R2 Tail-Risk Sell-off</i>).</li>
                    <li><b>Purging & Embargo (Méthode Marcos López de Prado) :</b> Lors de l'entraînement Walk-Forward glissant, les <b>25 dernières séances</b> (20 jours d'horizon cible + 5 jours d'embargo) sont systématiquement purgées avant chaque fenêtre de test pour empêcher toute fuite d'information future.</li>
                    <li><b>Live Tail Inference :</b> Les 25 séances les plus récentes (dont le futur à 20 jours est inconnu aujourd'hui) sont inférées en temps réel par le dernier modèle calibré.</li>
                    <li><b>Rétrécissement de Ledoit-Wolf :</b> Élimine l'instabilité d'inversion de la matrice de covariance empirique sous contraintes Long-Only (SLSQP).</li>
                    <li><b>Couverture Dynamique Black-Scholes (1973) :</b> Déclenchement automatique d'une protection Put 30 jours OTM 5% dès que la probabilité du régime R2 devient dominante.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )


# =====================================================================
# 6. BARRE LATÉRALE & ORCHESTRATION PRINCIPALE
# =====================================================================

def main():
    inject_custom_css()

    with st.sidebar:
        lang = st.radio("LANGUAGE // LANGUE", ["FR", "EN"], horizontal=True)
        st.session_state["lang"] = lang
        t = I18N[lang]

        st.markdown(f"### {t['sidebar_title']}")
        src_choice = st.radio(t["data_source"], [t["src_live"], t["src_demo"]])
        force_demo = (src_choice == t["src_demo"])

        if st.button(t["refresh_btn"]):
            st.cache_data.clear()
            st.rerun()

        default_tickers = ["SPY", "QQQ", "EZU", "VGK", "GLD", "TLT", "SHY"]
        selected_tickers = st.multiselect(t["universe_label"], default_tickers, default=default_tickers)

        start_date = st.date_input(
            t["start_date"],
            value=datetime.date(2023, 1, 1),
            max_value=datetime.date.today() - datetime.timedelta(days=90)
        )

        model_map = {
            "XGBoost Classifier (Gradient Boosting)": "xgb",
            "CatBoost Regime Engine": "cat",
            "Random Forest (Ensemble)": "rf",
            "Logistic Regression (Baseline)": "logreg"
        }
        model_label = st.selectbox(t["ml_model_label"], list(model_map.keys()))
        model_key = model_map[model_label]

        max_cap = st.slider(t["max_cap"], min_value=0.20, max_value=1.00, value=0.35, step=0.05)
        fee_bps = st.slider(t["fee_bps"], min_value=0, max_value=50, value=10, step=1)
        slip_bps = st.slider(t["slip_bps"], min_value=0, max_value=50, value=5, step=1)

    results = run_full_quant_pipeline(
        tickers=selected_tickers if selected_tickers else ["SPY", "QQQ", "GLD", "TLT"],
        start_date=start_date,
        model_key=model_key,
        max_weight=max_cap,
        fee_bps=fee_bps,
        slip_bps=slip_bps,
        force_demo=force_demo
    )

    if st.session_state["view"] == "landing":
        render_landing_page(I18N[st.session_state["lang"]], results)
    else:
        render_terminal_view(I18N[st.session_state["lang"]], results)


if __name__ == "__main__":
    main()