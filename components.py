"""Small, reusable Streamlit render helpers."""

import pandas as pd
import streamlit as st

from model import Signals


def render_header() -> None:
    st.markdown(
        "<div class='term-title'>"
        "<span style='font-size:1.3rem;font-weight:700;'>ORDER SKEW MONITOR</span>"
        "&nbsp;&nbsp;<span class='term-subtitle'>DELAYED DATA — PROXY MODEL, NOT ORDER-BOOK DEPTH</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)


def render_data_summary(ticker_label: str, bars: pd.DataFrame) -> None:
    last_price = float(bars["Close"].iloc[-1])
    st.markdown(
        f"<div class='term-panel' style='margin-bottom:10px;'>"
        f"<b>{ticker_label}</b>"
        f"&nbsp;&nbsp;|&nbsp;&nbsp;LAST <b>{last_price:,.2f}</b>"
        f"&nbsp;&nbsp;|&nbsp;&nbsp;BARS <b>{len(bars)}</b>"
        f"&nbsp;&nbsp;|&nbsp;&nbsp;RANGE {bars.index[0]} &rarr; {bars.index[-1]}"
        f"</div>",
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value_html: str, css_class: str = "") -> None:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value {css_class}">{value_html}</div></div>',
        unsafe_allow_html=True,
    )


def render_signal_row(sig: Signals) -> None:
    columns = st.columns(5)
    cells = [
        ("Avg Skew", f"{sig.avg:.3f}", "positive" if sig.avg > 0 else "negative"),
        ("Energy", f"{sig.energy:.3f}", "warning" if sig.energy > 0.05 else ""),
        ("Momentum", f"{sig.momentum:.4f}", "positive" if sig.momentum > 0 else "negative"),
        ("Volatility", f"{sig.volatility:.3f}", ""),
        ("Signal", sig.regime, {
            "BUY": "positive", "SELL": "negative", "HIGH VOL": "warning",
        }.get(sig.regime, "")),
    ]
    for column, (label, value, css_class) in zip(columns, cells):
        with column:
            render_metric_card(label, value, css_class)