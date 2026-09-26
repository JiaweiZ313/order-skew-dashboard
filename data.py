"""Market data access.

Uses yfinance for free, delayed OHLCV bars. There is no free source for
real bid/ask order-book depth, so this module only ever returns bars —
the skew model in model.py is responsible for turning bars into a proxy
"skew" field.
"""

import pandas as pd
import streamlit as st
import yfinance as yf

from config import CACHE_TTL_SECONDS


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_bars(ticker: str, interval: str, period: str) -> pd.DataFrame:
    """Fetch OHLCV bars for `ticker`, cached for CACHE_TTL_SECONDS.

    Returns an empty DataFrame if yfinance has no data for the requested
    interval/period combination (common cause: intraday intervals like "1m"
    only cover the last few days on Yahoo's side).
    """
    raw = yf.download(ticker, interval=interval, period=period, progress=False)

    if raw.empty:
        return raw

    # yfinance can return MultiIndex columns (ticker, field) — flatten them.
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    return raw.dropna()