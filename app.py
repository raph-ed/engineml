# =====================================================================
# 1. INJECTION DU DESIGN SYSTEM (TOTAL MATTE BLACK & BENTO GLASSMORPHISM)
# =====================================================================

def inject_custom_css():
    # Replier visuellement la sidebar sur la Landing Page pour avoir le rendu plein écran
    hide_sidebar_css = ""
    if st.session_state.get("view") == "landing":
        hide_sidebar_css = """
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        """

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        {hide_sidebar_css}

        html, body, [class*="css"], .stApp {{
            background-color: #050506 !important;
            color: #E6EDF3 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}

        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}
        .block-container {{
            padding-top: 2.2rem !important;
            padding-bottom: 2rem !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
            max-width: 1600px !important;
        }}

        section[data-testid="stSidebar"] {{
            background-color: #08080A !important;
            border-right: 1px solid #1F1F24 !important;
        }}

        /* Hero Styling (Colonne Gauche) */
        .hero-title {{
            font-size: clamp(2.4rem, 3.4vw, 3.35rem);
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.06;
            color: #FFFFFF;
            margin-bottom: 0.85rem;
            text-transform: uppercase;
        }}
        .hero-subtitle {{
            font-size: 1.12rem;
            font-weight: 400;
            color: #A1A1AA;
            margin-bottom: 0.9rem;
            line-height: 1.45;
        }}
        .hero-mono-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            letter-spacing: 0.06em;
            color: #D4D4D8;
            margin-bottom: 0.5rem;
            display: block;
        }}

        /* Cadre global du Terminal (st.container(border=True)) */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: linear-gradient(180deg, #0B0C10 0%, #07080A 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 14px !important;
            padding: 18px 22px !important;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85) !important;
        }}

        .terminal-window-header {{
            font-size: 0.95rem;
            font-weight: 500;
            color: #D4D4D8;
            padding-bottom: 12px;
            margin-bottom: 6px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }}

        /* Bento KPI Cards - Hauteur auto & vrais dégradés lumineux */
        .bento-card {{
            border-radius: 10px;
            padding: 14px 16px;
            min-height: 122px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            margin-bottom: 14px;
            box-sizing: border-box;
            backdrop-filter: blur(12px);
        }}
        .bento-cyan {{
            background: radial-gradient(120% 100% at 50% 0%, rgba(6, 182, 212, 0.28) 0%, rgba(11, 15, 20, 0.92) 75%);
            border: 1px solid rgba(6, 182, 212, 0.45);
            box-shadow: 0 0 24px rgba(6, 182, 212, 0.12);
        }}
        .bento-green {{
            background: radial-gradient(120% 100% at 50% 0%, rgba(16, 185, 129, 0.28) 0%, rgba(10, 18, 15, 0.92) 75%);
            border: 1px solid rgba(16, 185, 129, 0.45);
            box-shadow: 0 0 24px rgba(16, 185, 129, 0.12);
        }}
        .bento-amber {{
            background: radial-gradient(120% 100% at 50% 0%, rgba(245, 158, 11, 0.28) 0%, rgba(20, 14, 10, 0.92) 75%);
            border: 1px solid rgba(245, 158, 11, 0.45);
            box-shadow: 0 0 24px rgba(245, 158, 11, 0.12);
        }}
        .bento-red {{
            background: radial-gradient(120% 100% at 50% 0%, rgba(239, 68, 68, 0.30) 0%, rgba(22, 11, 11, 0.92) 75%);
            border: 1px solid rgba(239, 68, 68, 0.50);
            box-shadow: 0 0 24px rgba(239, 68, 68, 0.15);
        }}

        .kpi-label {{
            font-size: 0.68rem;
            font-weight: 600;
            letter-spacing: 0.06em;
            color: #D4D4D8;
            text-transform: uppercase;
            margin-bottom: 4px;
        }}
        .kpi-value {{
            font-family: 'Inter', sans-serif;
            font-size: clamp(1.2rem, 1.5vw, 1.55rem);
            font-weight: 700;
            line-height: 1.15;
            margin: 2px 0 6px 0;
            word-wrap: break-word;
        }}
        .kpi-sub {{
            font-size: 0.72rem;
            color: #A1A1AA;
            line-height: 1.3;
        }}

        /* Boîte interne du graphique Plotly */
        .panel-box {{
            background: #0D0E12;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 16px 20px;
            margin-top: 8px;
        }}

        /* Live Stats Bar on Landing */
        .stats-section-title {{
            font-size: 0.80rem;
            letter-spacing: 0.06em;
            color: #A1A1AA;
            font-weight: 600;
            text-transform: uppercase;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            margin-top: 4px;
        }}
        .live-stats-bar {{
            padding: 12px 0 18px 0;
            display: flex;
            justify-content: flex-start;
            gap: 28px;
            align-items: center;
            font-size: 0.92rem;
            color: #A1A1AA;
        }}
        .live-stats-bar b {{
            color: #FFFFFF;
            font-weight: 700;
        }}

        /* Bouton principal CTA */
        div.stButton > button {{
            background: rgba(24, 25, 32, 0.9) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.22) !important;
            border-radius: 8px !important;
            padding: 0.78rem 1.5rem !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            letter-spacing: 0.05em !important;
            width: 100% !important;
            transition: all 0.2s ease !important;
        }}
        div.stButton > button:hover {{
            border-color: #10B981 !important;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.25) !important;
            background: #181B24 !important;
        }}

        /* Onglets (Tabs) style Terminal */
        div[data-baseweb="tab-list"] {{
            gap: 24px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
            padding-bottom: 0px !important;
            margin-bottom: 14px !important;
        }}
        button[data-baseweb="tab"] {{
            font-family: 'Inter', sans-serif !important;
            font-size: 0.90rem !important;
            font-weight: 500 !important;
            color: #71717A !important;
            padding: 8px 4px 10px 4px !important;
            background: transparent !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }}
        div[data-baseweb="tab-highlight"] {{
            background-color: #10B981 !important;
            height: 2px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
# =====================================================================
# 4. VUE 1 : LANDING PAGE VITRINE HAUTE TECHNOLOGIE + APERÇU TERMINAL
# =====================================================================

def render_landing_page(t, results):
    col_left, col_right = st.columns([1.0, 1.18], gap="large")

    with col_left:
        st.markdown(f'<div class="hero-title">{t["hero_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-subtitle">{t["hero_sub"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-mono-badge">{t["hero_badge"]}</div>', unsafe_allow_html=True)

        render_interactive_3d_globe()

        st.markdown(
            f"""
            <div class="stats-section-title">{t["stats_header"]}</div>
            <div class="live-stats-bar">
                <div>Volume Traité : <b>$1.2B+</b></div>
                <div>Actifs Analysés : <b>18+</b></div>
                <div>Précision Machine : <b>{results['oos_acc']*100:.1f}%</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(t["cta_enter"], key="btn_enter_terminal"):
            st.session_state["view"] = "terminal"
            st.rerun()

    with col_right:
        # Vrai conteneur encadré pour la fenêtre "Terminal"
        with st.container(border=True):
            st.markdown('<div class="terminal-window-header">Terminal</div>', unsafe_allow_html=True)

            preview_tabs = st.tabs(["Aperçu", "Allocations", "Backtest", "Options"])

            with preview_tabs[0]:
                render_kpi_row(t, results)
                with st.container(border=True):
                    fig_preview = build_regime_glow_chart(
                        results["df_view"],
                        results["preds"],
                        "Prix de l'Actif Sous-Jacent & Régimes Estimés"
                    )
                    st.plotly_chart(fig_preview, use_container_width=True, key="landing_preview_chart")

            with preview_tabs[1]:
                c_p1, c_p2 = st.columns(2)
                palette = ["#10B981", "#06B6D4", "#3B82F6", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899"]
                with c_p1:
                    sw = results["static_weights"]
                    fig_s = go.Figure(go.Pie(
                        labels=sw.index, values=sw.values, hole=0.58,
                        marker=dict(colors=palette, line=dict(color="#050506", width=2))
                    ))
                    fig_s.update_layout(
                        title="Allocation Statique", template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)", height=320, margin=dict(l=10, r=10, t=40, b=10)
                    )
                    st.plotly_chart(fig_s, use_container_width=True, key="land_pie_s")
                with c_p2:
                    dw = results["dynamic_weights"]
                    fig_d = go.Figure(go.Pie(
                        labels=dw.index, values=dw.values, hole=0.58,
                        marker=dict(colors=palette, line=dict(color="#050506", width=2))
                    ))
                    fig_d.update_layout(
                        title="Allocation Dynamique", template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)", height=320, margin=dict(l=10, r=10, t=40, b=10)
                    )
                    st.plotly_chart(fig_d, use_container_width=True, key="land_pie_d")

            with preview_tabs[2]:
                bt_df = results["bt_df"]
                fig_bt = go.Figure()
                colors_bt = {"Dynamic Quant Engine": "#10B981", "Benchmark 60/40": "#06B6D4", "S&P 500 Buy & Hold": "#9CA3AF"}
                for col in bt_df.columns:
                    fig_bt.add_trace(go.Scatter(
                        x=bt_df.index, y=bt_df[col], mode="lines", name=col,
                        line=dict(color=colors_bt.get(col, "#FFFFFF"), width=2.2)
                    ))
                fig_bt.update_layout(
                    title=t["chart_bt_title"], template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    height=340, margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified"
                )
                st.plotly_chart(fig_bt, use_container_width=True, key="land_bt")

            with preview_tabs[3]:
                opt_df = results["options_df"]
                fig_opt = go.Figure()
                fig_opt.add_trace(go.Scatter(
                    x=opt_df.index, y=opt_df["Put_Hedged_Portfolio"],
                    mode="lines", name="Put Hedged Portfolio", line=dict(color="#10B981", width=2.2)
                ))
                fig_opt.add_trace(go.Scatter(
                    x=opt_df.index, y=opt_df["Unhedged_SPY"],
                    mode="lines", name="Unhedged SPY", line=dict(color="#EF4444", width=1.5, dash="dot")
                ))
                fig_opt.update_layout(
                    title=t["chart_opt_title"], template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    height=340, margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified"
                )
                st.plotly_chart(fig_opt, use_container_width=True, key="land_opt")


# =====================================================================
# 5. CARTES KPI BENTO GRID
# =====================================================================

def render_kpi_row(t, results):
    reg = results["current_regime"]
    p0 = float(results["last_probs"]["P0"]) * 100
    p2 = float(results["last_probs"]["P2"]) * 100
    vix = results["last_vix"]
    spot = results["last_spot"]

    reg_meta = {
        0: (t["regime_0_name"], t["regime_0_desc"], "bento-green", "#34D399"),
        1: (t["regime_1_name"], t["regime_1_desc"], "bento-cyan", "#38BDF8"),
        2: (t["regime_2_name"], t["regime_2_desc"], "bento-red", "#F87171"),
    }[reg]

    c1, c2, c3, c4 = st.columns([1.15, 1, 1, 0.9], gap="small")
    with c1:
        st.markdown(
            f"""
            <div class="bento-card {reg_meta[2]}">
                <div class="kpi-label">{t["kpi_1_title"]}</div>
                <div class="kpi-value" style="color:{reg_meta[3]}; font-size:1.22rem;">{reg_meta[0]}</div>
                <div class="kpi-sub">{reg_meta[1]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="bento-card bento-green">
                <div class="kpi-label">PROBABILITÉ HAUSSIÈRE</div>
                <div class="kpi-value" style="color:#34D399;">{p0:.1f}%</div>
                <div class="kpi-sub">Confidence Score: {"High" if p0 > 50 else "Moderate"}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        tail_status = "CRITICAL" if p2 > 45 else ("ELEVATED" if p2 > 20 else "CONTAINED")
        card_cls = "bento-red" if p2 > 45 else "bento-amber"
        val_col = "#F87171" if p2 > 45 else "#FB923C"
        st.markdown(
            f"""
            <div class="bento-card {card_cls}">
                <div class="kpi-label">PROBABILITÉ DE BAISSE</div>
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
                <div class="kpi-sub">SPY Ref: <b>${spot:.1f}</b></div>
            </div>
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
    <meta charset="utf-8">
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script src="https://unpkg.com/topojson-client@3"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        * {
            box-sizing: border-box;
        }
        body {
            margin: 0;
            background: transparent;
            overflow: hidden;
            font-family: 'Inter', -apple-system, sans-serif;
            display: flex;
            justify-content: flex-start;
            align-items: center;
            height: 410px;
        }
        #globe-wrapper {
            position: relative;
            width: 100%;
            height: 410px;
            display: flex;
            align-items: center;
        }
        canvas {
            cursor: grab;
            margin-left: -10px;
        }
        canvas:active {
            cursor: grabbing;
        }
        .flash-card {
            position: absolute;
            top: 52px;
            right: 8px;
            width: 285px;
            background: rgba(16, 17, 22, 0.88);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 10px;
            padding: 12px 14px;
            color: #E6EDF3;
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.85), 0 0 0 1px rgba(255,255,255,0.04);
            pointer-events: none;
            transition: all 0.25s ease;
        }
        .flash-header {
            font-family: 'JetBrains Mono', monospace;
            font-size: 9.8px;
            font-weight: 700;
            color: #F4F4F5;
            letter-spacing: 0.02em;
            border-bottom: 1px solid rgba(255, 255, 255, 0.09);
            padding-bottom: 6px;
            margin-bottom: 8px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .flash-body {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }
        .flash-metrics {
            font-family: 'JetBrains Mono', monospace;
            font-size: 10.2px;
            line-height: 1.55;
            width: 55%;
        }
        .m-row {
            display: flex;
            justify-content: space-between;
        }
        .c-green { color: #10B981; font-weight: 600; }
        .c-red { color: #EF4444; font-weight: 600; }
        .dot-g { color: #10B981; margin-right: 3px; }
        .dot-r { color: #EF4444; margin-right: 3px; }
    </style>
    </head>
    <body>
    <div id="globe-wrapper">
        <canvas id="globeCanvas" width="620" height="410"></canvas>
        <div class="flash-card" id="flashCard">
            <div class="flash-header" id="flashTitle">FLASH INFO // US Market - Inflation Data Impact</div>
            <div class="flash-body">
                <svg width="112" height="54" viewBox="0 0 120 58">
                    <defs>
                        <linearGradient id="sparkGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stop-color="#10B981" stop-opacity="0.42"/>
                            <stop offset="100%" stop-color="#10B981" stop-opacity="0.0"/>
                        </linearGradient>
                    </defs>
                    <!-- Grille de fond miniature -->
                    <line x1="0" y1="15" x2="120" y2="15" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
                    <line x1="0" y1="32" x2="120" y2="32" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
                    <line x1="0" y1="49" x2="120" y2="49" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
                    <!-- Courbe Sparkline bicolore (début rouge puis rallye vert comme sur la maquette) -->
                    <path d="M2,48 L16,42 L28,45 L42,35 L56,28 L72,34 L86,18 L100,24 L116,10 L116,56 L2,56 Z" fill="url(#sparkGrad)"/>
                    <path d="M2,48 L16,42 L28,45 L42,35" fill="none" stroke="#EF4444" stroke-width="2" stroke-linecap="round"/>
                    <path d="M42,35 L56,28 L72,34 L86,18 L100,24 L116,10" fill="none" stroke="#10B981" stroke-width="2.2" stroke-linecap="round"/>
                </svg>
                <div class="flash-metrics">
                    <div class="m-row"><span><span class="dot-g">•</span>15.55%</span><span class="c-green">158.85B</span></div>
                    <div class="m-row"><span><span class="dot-g">•</span>33.77%</span><span class="c-green">+33.59B</span></div>
                    <div class="m-row"><span><span class="dot-r">•</span>29.23%</span><span class="c-red">+35.93B</span></div>
                    <div class="m-row"><span><span class="dot-r">•</span>94.23%</span><span class="c-red">+37.92B</span></div>
                </div>
            </div>
        </div>
    </div>

    <script>
    const canvas = document.getElementById('globeCanvas');
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const W = 620, H = 410;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    canvas.style.width = W + 'px';
    canvas.style.height = H + 'px';
    ctx.scale(dpr, dpr);

    const cx = 215, cy = 205, R = 154;

    // Angle initial centré sur l'Atlantique / Amériques / Europe (comme sur la maquette)
    let yaw = 42;
    let pitch = -14;
    let isDragging = false, prevX = 0, prevY = 0;

    const projection = d3.geoOrthographic()
        .scale(R)
        .translate([cx, cy])
        .clipAngle(90);

    const path = d3.geoPath(projection, ctx);
    const graticule = d3.geoGraticule10();

    let landFeature = null;
    let landDots = [];

    // Génération de la grille de points à l'intérieur des continents
    function buildLandDots(land) {
        const dots = [];
        const step = 2.6;
        for (let lat = -60; lat <= 75; lat += step) {
            const cosLat = Math.cos(lat * Math.PI / 180);
            const lonStep = step / Math.max(0.28, cosLat);
            for (let lon = -180; lon < 180; lon += lonStep) {
                if (d3.geoContains(land, [lon, lat])) {
                    dots.push([lon, lat]);
                }
            }
        }
        return dots;
    }

    // Chargement de la vraie carte du monde (TopoJSON 110m)
    fetch("https://cdn.jsdelivr.net/npm/world-atlas@2/land-110m.json")
        .then(r => r.json())
        .then(world => {
            landFeature = topojson.feature(world, world.objects.land);
            landDots = buildLandDots(landFeature);
        })
        .catch(() => {
            // Fallback immédiat si hors-ligne
            landDots = [];
        });

    // Hotspots (coordonnées [lon, lat] exactes de la maquette)
    const hotspots = [
        { coords: [-77.0, 38.9], size: 9.5, primary: true, title: "FLASH INFO // US Market - Inflation Data Impact" },
        { coords: [-118.2, 34.0], size: 6.5, primary: false, title: "FLASH INFO // Silicon Valley - Tech Liquidity Flow" },
        { coords: [-99.1, 19.4], size: 5.5, primary: false, title: "FLASH INFO // LatAm North - FX Carry Trade" },
        { coords: [-46.6, -23.5], size: 7.5, primary: false, title: "FLASH INFO // EM Commodities - Brazil & LatAm Desk" },
        { coords: [-58.4, -34.6], size: 5.5, primary: false, title: "FLASH INFO // Southern Cone - Sovereign Debt Spread" },
        { coords: [-0.1, 51.5], size: 8.5, primary: false, title: "FLASH INFO // Eurozone & UK - Monetary Feed" },
        { coords: [18.4, -33.9], size: 5.5, primary: false, title: "FLASH INFO // EMEA Desk - Gold & Precious Metals" },
        { coords: [45.0, 24.0], size: 6.5, primary: false, title: "FLASH INFO // Middle East - Energy & Commodity Shock" },
        { coords: [121.5, 25.0], size: 7.5, primary: false, title: "FLASH INFO // APAC - Semiconductor Supply Chain" }
    ];

    canvas.addEventListener('mousedown', e => {
        isDragging = true;
        prevX = e.clientX;
        prevY = e.clientY;
    });
    window.addEventListener('mouseup', () => { isDragging = false; });
    window.addEventListener('mousemove', e => {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;

        if (isDragging) {
            yaw += (e.clientX - prevX) * 0.35;
            pitch = Math.max(-45, Math.min(45, pitch - (e.clientY - prevY) * 0.35));
            prevX = e.clientX;
            prevY = e.clientY;
        }

        for (const h of hotspots) {
            if (h.visible && Math.hypot(mx - h.sx, my - h.sy) < 16) {
                document.getElementById('flashTitle').innerText = h.title;
                break;
            }
        }
    });

    let pulse = 0;

    function drawOrbits() {
        // Anneau orbital 1 (pointillés fins inclinés)
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(-0.38);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.16)";
        ctx.setLineDash([2, 5]);
        ctx.lineWidth = 1.1;
        ctx.beginPath();
        ctx.ellipse(0, 0, R + 32, R + 8, 0, 0, Math.PI * 2);
        ctx.stroke();

        // Anneau orbital 2 (croisé)
        ctx.rotate(0.72);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.10)";
        ctx.setLineDash([4, 6]);
        ctx.beginPath();
        ctx.ellipse(0, 0, R + 18, R + 34, 0, 0, Math.PI * 2);
        ctx.stroke();

        // Arc externe subtil à gauche
        ctx.rotate(-0.34);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.12)";
        ctx.setLineDash([1.5, 4]);
        ctx.beginPath();
        ctx.arc(0, 0, R + 24, Math.PI * 0.65, Math.PI * 1.38);
        ctx.stroke();
        ctx.restore();
    }

    function draw() {
        ctx.clearRect(0, 0, W, H);

        // Rotation très douce pour garder l'Amérique et l'Europe bien visibles
        if (!isDragging) {
            yaw += 0.08;
        }
        pulse += 0.055;
        projection.rotate([yaw, pitch, 0]);

        // 1. Halo atmosphérique externe autour du globe
        const atmo = ctx.createRadialGradient(cx, cy, R * 0.85, cx, cy, R + 28);
        atmo.addColorStop(0, "rgba(255, 255, 255, 0.06)");
        atmo.addColorStop(0.6, "rgba(255, 255, 255, 0.02)");
        atmo.addColorStop(1, "rgba(0, 0, 0, 0)");
        ctx.fillStyle = atmo;
        ctx.beginPath();
        ctx.arc(cx, cy, R + 28, 0, Math.PI * 2);
        ctx.fill();

        // 2. Anneaux orbitaux en pointillés
        drawOrbits();

        // 3. Corps de la sphère (éclairage 3D anthracite/argenté en haut à gauche)
        const sphereGrad = ctx.createRadialGradient(cx - 52, cy - 52, R * 0.08, cx, cy, R);
        sphereGrad.addColorStop(0, "#2A2D35");
        sphereGrad.addColorStop(0.45, "#12141A");
        sphereGrad.addColorStop(0.85, "#07080B");
        sphereGrad.addColorStop(1, "#030305");
        ctx.fillStyle = sphereGrad;
        ctx.beginPath();
        ctx.arc(cx, cy, R, 0, Math.PI * 2);
        ctx.fill();

        // 4. Grille géodésique (latitudes / longitudes)
        ctx.beginPath();
        path(graticule);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.07)";
        ctx.lineWidth = 0.65;
        ctx.stroke();

        // 5. Remplissage et contour des continents
        if (landFeature) {
            ctx.beginPath();
            path(landFeature);
            ctx.fillStyle = "rgba(200, 210, 225, 0.07)";
            ctx.fill();
            ctx.strokeStyle = "rgba(220, 230, 242, 0.28)";
            ctx.lineWidth = 0.85;
            ctx.stroke();
        }

        // 6. Matrice de micro-points sur les continents (effet Digital Twin)
        const centerLonLat = [-yaw, -pitch];
        ctx.fillStyle = "rgba(230, 236, 245, 0.58)";
        for (let i = 0; i < landDots.length; i++) {
            const d = landDots[i];
            const dist = d3.geoDistance(d, centerLonLat);
            if (dist < 1.52) {
                const pt = projection(d);
                if (pt) {
                    ctx.fillRect(pt[0], pt[1], 1.35, 1.35);
                }
            }
        }

        // 7. Bordure lumineuse (Rim Light) de la sphère
        ctx.beginPath();
        ctx.arc(cx, cy, R, 0, Math.PI * 2);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.26)";
        ctx.lineWidth = 1.25;
        ctx.stroke();

        // 8. Hotspots rouges lumineux + connecteur vers la carte Flash Info
        for (const h of hotspots) {
            const dist = d3.geoDistance(h.coords, centerLonLat);
            if (dist < 1.48) {
                const pt = projection(h.coords);
                if (!pt) continue;
                h.sx = pt[0];
                h.sy = pt[1];
                h.visible = true;

                const glowR = h.size * (2.7 + 0.45 * Math.sin(pulse));
                const g = ctx.createRadialGradient(pt[0], pt[1], 1, pt[0], pt[1], glowR);
                g.addColorStop(0, "rgba(239, 68, 68, 0.95)");
                g.addColorStop(0.35, "rgba(239, 68, 68, 0.45)");
                g.addColorStop(0.7, "rgba(239, 68, 68, 0.12)");
                g.addColorStop(1, "rgba(239, 68, 68, 0)");

                ctx.fillStyle = g;
                ctx.beginPath();
                ctx.arc(pt[0], pt[1], glowR, 0, Math.PI * 2);
                ctx.fill();

                // Cœur incandescent blanc-rosé
                ctx.fillStyle = "#FECACA";
                ctx.beginPath();
                ctx.arc(pt[0], pt[1], h.primary ? 3.8 : 2.8, 0, Math.PI * 2);
                ctx.fill();
            } else {
                h.visible = false;
            }
        }

        requestAnimationFrame(draw);
    }

    draw();
    </script>
    </body>
    </html>
    """
    components.html(globe_html, height=415)
# =====================================================================
# 3. GRAPHIQUES PLOTLY HAUTE PRÉCISION (COURBE TRICOLORE + HALO NÉON)
# =====================================================================

def build_regime_glow_chart(df_view, preds, title):
    fig = go.Figure()
    spy = df_view["SPY"]

    # Tracé de base continu (SPY Price)
    fig.add_trace(go.Scatter(
        x=df_view.index,
        y=spy,
        mode="lines",
        line=dict(color="rgba(255, 255, 255, 0.22)", width=1.2),
        name="SPY Price",
        hoverinfo="skip"
    ))

    # Configuration : (code_regime, label, couleur_ligne, couleur_halo, couleur_remplissage)
    regime_cfg = [
        (0, "Bullish (R0)", "#10B981", "rgba(16, 185, 129, 0.28)", "rgba(16, 185, 129, 0.11)"),
        (1, "Neutral (R1)", "#06B6D4", "rgba(6, 182, 212, 0.28)", "rgba(6, 182, 212, 0.09)"),
        (2, "Sell-off (R2)", "#EF4444", "rgba(239, 68, 68, 0.35)", "rgba(239, 68, 68, 0.15)"),
    ]

    for r_code, r_label, hex_col, glow_rgba, fill_rgba in regime_cfg:
        mask = (preds == r_code) | (preds.shift(1) == r_code)
        y_masked = spy.where(mask, np.nan)

        # 1. Couche de Halo (Glow externe autour de la courbe, non affichée dans la légende)
        fig.add_trace(go.Scatter(
            x=df_view.index,
            y=y_masked,
            mode="lines",
            line=dict(color=glow_rgba, width=7.5),
            showlegend=False,
            hoverinfo="skip"
        ))

        # 2. Courbe principale nette + remplissage dégradé vers le bas
        fig.add_trace(go.Scatter(
            x=df_view.index,
            y=y_masked,
            mode="lines",
            name=r_label,
            line=dict(color=hex_col, width=2.3),
            fill="tozeroy",
            fillcolor=fill_rgba,
            hovertemplate=f"<b>{r_label}</b>: $%{{y:.2f}}<extra></extra>"
        ))

    y_min = float(spy.min()) * 0.94
    y_max = float(spy.max()) * 1.04

    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(family="Inter, sans-serif", size=15, color="#F4F4F5"),
            x=0.0,
            y=0.96,
            xanchor="left",
            yanchor="top"
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=355,
        margin=dict(l=8, r=8, t=52, b=8),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            bgcolor="rgba(16, 17, 22, 0.85)",
            bordercolor="rgba(255, 255, 255, 0.10)",
            borderwidth=1,
            font=dict(family="Inter, sans-serif", size=11, color="#D4D4D8")
        ),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            zeroline=False,
            showline=True,
            linecolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(family="JetBrains Mono, monospace", size=10.5, color="#9CA3AF")
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            range=[y_min, y_max],
            zeroline=False,
            tickfont=dict(family="JetBrains Mono, monospace", size=10.5, color="#9CA3AF")
        )
    )
    return fig
