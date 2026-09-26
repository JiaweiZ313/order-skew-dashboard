"""Skew field model and signal computation.

The "skew field" is a (time x price_level) array in [-1, 1] used to drive
the 3D visualization. Since real order-book depth isn't freely available,
`build_skew_field` derives a proxy from each bar's direction and volume
rather than true bid/ask imbalance. Treat the output as an approximation
of buy/sell pressure, not a reconstruction of the order book.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter

from config import AVG_BUY_THRESHOLD, AVG_SELL_THRESHOLD, ENERGY_HIGH_VOL_THRESHOLD


def build_skew_field(bars: pd.DataFrame, n_price: int) -> np.ndarray:
    """Turn OHLCV bars into a (n_time, n_price) proxy skew field.

    Each bar's normalized volume is spread across a Gaussian window of
    price levels centered on that bar's high/low midpoint, signed by
    whether the bar closed up (+1) or down (-1). The result is smoothed
    per-row and rescaled so the whole field fits in [-1, 1].
    """
    n_time = len(bars)
    if n_time == 0:
        return np.zeros((1, n_price))

    price_lo, price_hi = bars["Low"].min(), bars["High"].max()
    if price_hi == price_lo:
        price_hi = price_lo + 1e-6
    price_bins = np.linspace(price_lo, price_hi, n_price)
    min_spread = (price_hi - price_lo) / n_price

    opens = bars["Open"].to_numpy()
    closes = bars["Close"].to_numpy()
    highs = bars["High"].to_numpy()
    lows = bars["Low"].to_numpy()
    norm_volume = bars["Volume"].to_numpy()
    norm_volume = norm_volume / (norm_volume.max() + 1e-9)

    field = np.zeros((n_time, n_price))
    for t in range(n_time):
        direction = 1.0 if closes[t] >= opens[t] else -1.0
        center = (highs[t] + lows[t]) / 2
        spread = max(highs[t] - lows[t], min_spread)

        weights = np.exp(-0.5 * ((price_bins - center) / spread) ** 2)
        weights /= weights.sum() + 1e-9

        field[t] = gaussian_filter(direction * norm_volume[t] * weights, sigma=1.0)

    peak = np.max(np.abs(field)) + 1e-9
    return field / peak


@dataclass
class Signals:
    avg: float
    energy: float
    buy_pressure: float
    sell_pressure: float
    momentum: float
    volatility: float
    regime: str

    def as_dict(self) -> dict:
        return {
            "avg": self.avg,
            "energy": self.energy,
            "buy": self.buy_pressure,
            "sell": self.sell_pressure,
            "momentum": self.momentum,
            "vol": self.volatility,
            "regime": self.regime,
        }


def compute_signals(field: np.ndarray, t: int) -> Signals:
    """Summarize the skew field at time step `t` into headline signals."""
    row = field[t]
    prev_row = field[t - 1] if t > 0 else row

    avg = float(np.mean(row))
    energy = float(np.mean(row ** 2))

    if energy > ENERGY_HIGH_VOL_THRESHOLD:
        regime = "HIGH VOL"
    elif avg > AVG_BUY_THRESHOLD:
        regime = "BUY"
    elif avg < AVG_SELL_THRESHOLD:
        regime = "SELL"
    else:
        regime = "NEUTRAL"

    return Signals(
        avg=avg,
        energy=energy,
        buy_pressure=float(np.sum(row[row > 0])),
        sell_pressure=float(abs(np.sum(row[row < 0]))),
        momentum=float(np.mean(row - prev_row)),
        volatility=float(np.std(row)),
        regime=regime,
    )