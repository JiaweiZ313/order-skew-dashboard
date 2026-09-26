"""Static configuration for the Order Skew dashboard."""

TICKERS = {
    "Nasdaq-100 Futures (NQ=F)": "NQ=F",
    "Micro Nasdaq-100 Futures (MNQ=F)": "MNQ=F",
    "S&P 500 Futures (ES=F)": "ES=F",
    "Micro S&P 500 Futures (MES=F)": "MES=F",
}

INTERVALS = {
    "1m": "1m",
    "2m": "2m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "60m",
}

LOOKBACK_PERIODS = ["1d", "5d", "1mo", "3mo"]

COLORSCALES = {
    "Amber": [
        [0.0, "#1a1000"], [0.25, "#7a4a00"], [0.5, "#0a0a0a"],
        [0.75, "#005f5f"], [1.0, "#00e0e0"],
    ],
    "Mono": [
        [0.0, "#3a3a3a"], [0.5, "#0a0a0a"], [1.0, "#e8e8e8"],
    ],
    "Plasma": "Plasma",
}

# Signal classification thresholds — tuned for the normalized [-1, 1] proxy
# field, not for genuine order-book imbalance. Recalibrate if you swap in a
# real depth feed later.
ENERGY_HIGH_VOL_THRESHOLD = 0.05
AVG_BUY_THRESHOLD = 0.03
AVG_SELL_THRESHOLD = -0.03

CACHE_TTL_SECONDS = 60

# Bloomberg-style terminal theme: black background, amber primary values,
# sharp square panels, dense monospace layout — no gradients, no glow,
# no decorative letter-spacing.
BG = "#000000"
PANEL_BG = "#0c0c0c"
BORDER = "#333333"
AMBER = "#ff9900"
CYAN = "#00cccc"
WHITE = "#e0e0e0"
GREY = "#888888"
RED = "#ff4d4d"
GREEN = "#00c853"

THEME_CSS = f"""
<style>
html, body, [class*="css"] {{
    font-family: 'Consolas', 'Courier New', monospace;
    background-color: {BG};
    color: {WHITE};
}}
.main {{ background-color: {BG}; }}
div[data-testid="stSidebar"] {{
    background-color: {PANEL_BG};
    border-right: 1px solid {BORDER};
}}
.term-panel {{
    background: {PANEL_BG};
    border: 1px solid {BORDER};
    border-radius: 0px;
    padding: 6px 10px;
}}
.metric-card {{
    background: {PANEL_BG};
    border: 1px solid {BORDER};
    border-radius: 0px;
    padding: 8px 12px;
    text-align: left;
}}
.metric-label {{
    font-size: 0.7rem;
    color: {GREY};
    text-transform: uppercase;
    border-bottom: 1px solid {BORDER};
    padding-bottom: 3px;
    margin-bottom: 4px;
}}
.metric-value {{
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    color: {AMBER};
}}
.metric-value.positive {{ color: {GREEN}; }}
.metric-value.negative {{ color: {RED}; }}
.metric-value.warning  {{ color: {AMBER}; }}
.term-title {{
    font-family: 'Consolas', 'Courier New', monospace;
    color: {AMBER};
    border-bottom: 1px solid {BORDER};
    padding-bottom: 6px;
}}
.term-subtitle {{
    color: {GREY};
    font-size: 0.75rem;
}}
</style>
"""