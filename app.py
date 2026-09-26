"""Dynamic Order Skew Evolution — live (delayed) market data dashboard.

Data source: yfinance (free, delayed OHLCV bars). There is no free source
for real bid/ask order-book depth, so the "skew" surface here is a proxy
built from bar direction and volume (see model.build_skew_field), not a
genuine reconstruction of the order book.
"""

import pandas as pd
import streamlit as st

import components
import viz
from config import COLORSCALES, INTERVALS, LOOKBACK_PERIODS, THEME_CSS, TICKERS
from data import fetch_bars
from model import build_skew_field, compute_signals


def render_sidebar() -> dict:
    """Render sidebar controls and return the selected settings."""
    with st.sidebar:
        st.markdown("### ⚙️ Data Settings")
        ticker_label = st.selectbox("Instrument", list(TICKERS.keys()))
        interval_label = st.selectbox("Bar Interval", list(INTERVALS.keys()), index=2)
        period = st.selectbox("Lookback Period", LOOKBACK_PERIODS, index=1)
        n_price = st.slider("Price Levels (proxy resolution)", 10, 50, 30)
        window = st.slider("Rolling Window", 5, 60, 20)
        colorscale = st.selectbox("Color Scale", list(COLORSCALES.keys()))
        st.caption(
            "Data via yfinance — free, delayed. Skew is a volume/direction "
            "proxy, not real order-book depth."
        )
    return dict(
        ticker_label=ticker_label,
        ticker=TICKERS[ticker_label],
        interval=INTERVALS[interval_label],
        period=period,
        n_price=n_price,
        window=window,
        colorscale=colorscale,
    )


def render_signal_table(field, bars: pd.DataFrame) -> None:
    n_time = field.shape[0]
    step = max(1, n_time // 20)
    sample_indices = range(0, n_time, step)

    rows = [compute_signals(field, t).as_dict() for t in sample_indices]
    sig_df = pd.DataFrame(rows)
    sig_df.index = [
        bars.index[i].strftime("%H:%M") if i < len(bars.index) else f"T+{i}"
        for i in sample_indices
    ]
    st.dataframe(sig_df.round(4), use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Dynamic Order Skew Evolution — Live", layout="wide")
    st.markdown(THEME_CSS, unsafe_allow_html=True)

    settings = render_sidebar()

    components.render_header()

    with st.spinner("Fetching bars..."):
        bars = fetch_bars(settings["ticker"], settings["interval"], settings["period"])

    if bars.empty:
        st.error(
            f"No data returned for {settings['ticker']} at "
            f"interval={settings['interval']}, period={settings['period']}. "
            f"Try a different combination — yfinance limits how far back "
            f"intraday intervals go (e.g. 1m only covers the last few days)."
        )
        st.stop()

    field = build_skew_field(bars, settings["n_price"])
    latest_signals = compute_signals(field, field.shape[0] - 1)

    components.render_data_summary(settings["ticker_label"], bars)
    components.render_signal_row(latest_signals)

    st.markdown("<br>", unsafe_allow_html=True)
    surface_fig = viz.build_surface_figure(field, settings["window"], settings["colorscale"])
    st.plotly_chart(surface_fig, use_container_width=True)

    with st.expander("📊 Full Field Heatmap"):
        st.plotly_chart(viz.build_heatmap_figure(field), use_container_width=True)

    with st.expander("📈 Signal Table"):
        render_signal_table(field, bars)

    with st.expander("🕯️ Raw Price Bars"):
        st.dataframe(bars.tail(50), use_container_width=True)


if __name__ == "__main__":
    main()