# Order Skew Dashboard

Streamlit dashboard visualizing a dynamic "order skew" surface for index futures,
rendered as a 3D field over price levels and time.

## Caveat on the data

Bars come from [yfinance](https://pypi.org/project/yfinance/) — free and delayed.
There is no free source for real bid/ask order-book depth, so the skew surface is a
**proxy** built from bar direction and volume (see `model.build_skew_field`), not a
genuine reconstruction of the order book. Signal thresholds in `config.py` are tuned
for that normalized proxy field and would need recalibration against a real depth feed.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Layout

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit entry point, sidebar controls, page layout |
| `config.py` | Tickers, intervals, colorscales, thresholds, terminal theme CSS |
| `data.py` | Cached yfinance OHLCV fetching |
| `model.py` | Skew field construction and signal classification |
| `viz.py` | Plotly surface and chart rendering |
| `components.py` | Reusable metric/panel HTML components |
