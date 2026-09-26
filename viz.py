"""Plotly figure builders for the skew dashboard."""

import numpy as np
import plotly.graph_objects as go

from config import AMBER, COLORSCALES, GREY

AXIS_FONT = dict(color=GREY, size=9, family="Consolas, Courier New, monospace")
TICK_FONT = dict(color=GREY, size=8, family="Consolas, Courier New, monospace")
GRID_COLOR = "rgba(255,255,255,0.08)"


def _colorbar() -> dict:
    return dict(thickness=8, len=0.5, x=1.0,
                tickfont=dict(color=GREY, size=8, family="Consolas, Courier New, monospace"))


def _surface(z: np.ndarray, x: np.ndarray, y: np.ndarray, colorscale) -> go.Surface:
    return go.Surface(
        z=z, x=x, y=y,
        colorscale=colorscale, cmin=-1, cmax=1, showscale=True,
        colorbar=_colorbar(),
        lighting=dict(ambient=0.6, diffuse=0.8, specular=0.3, roughness=0.5),
        lightposition=dict(x=100, y=200, z=300),
    )


def build_surface_figure(field: np.ndarray, window: int, colorscale_name: str) -> go.Figure:
    """Animated 3D surface: x=price level, y=time, z=skew, with a rolling
    window and a play/pause + scrub-slider control."""
    n_time, n_price = field.shape
    price_axis = np.arange(n_price)
    colorscale = COLORSCALES.get(colorscale_name, "Amber")

    frames = []
    for t in range(n_time):
        t_start = max(0, t - window)
        frames.append(go.Frame(
            name=str(t),
            data=[_surface(
                z=field[t_start:t + 1],
                x=price_axis,
                y=np.arange(t_start, t + 1),
                colorscale=colorscale,
            )],
        ))

    fig = go.Figure(
        data=[_surface(field[0:1], price_axis, np.array([0]), colorscale)],
        frames=frames,
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=20, b=0),
        height=480,
        scene=dict(
            bgcolor="#000000",
            xaxis=dict(title=dict(text="Price Level", font=AXIS_FONT),
                       gridcolor=GRID_COLOR, tickfont=TICK_FONT),
            yaxis=dict(title=dict(text="Time Step", font=AXIS_FONT),
                       gridcolor=GRID_COLOR, tickfont=TICK_FONT),
            zaxis=dict(title=dict(text="Order Skew (proxy)", font=AXIS_FONT),
                       gridcolor=GRID_COLOR, range=[-1, 1], tickfont=TICK_FONT),
            camera=dict(eye=dict(x=1.6, y=-1.6, z=1.0)),
        ),
        updatemenus=[_play_pause_buttons()],
        sliders=[_frame_slider(n_time)],
    )
    return fig


def _play_pause_buttons() -> dict:
    return dict(
        type="buttons", showactive=False, x=0.05, y=0.0,
        bgcolor="#0c0c0c", bordercolor="#333333",
        font=dict(color=AMBER, family="Consolas, Courier New, monospace", size=10),
        buttons=[
            dict(label="▶  PLAY", method="animate",
                 args=[None, dict(frame=dict(duration=120, redraw=True),
                                   transition=dict(duration=0),
                                   fromcurrent=True, mode="immediate")]),
            dict(label="⏸  PAUSE", method="animate",
                 args=[[None], dict(frame=dict(duration=0, redraw=False),
                                     transition=dict(duration=0), mode="immediate")]),
        ],
    )


def _frame_slider(n_time: int) -> dict:
    return dict(
        active=0,
        currentvalue=dict(prefix="Frame: ", font=AXIS_FONT),
        pad=dict(t=10, b=5),
        bgcolor="#0c0c0c", bordercolor="#333333",
        font=dict(color=GREY, size=8, family="Consolas, Courier New, monospace"),
        steps=[
            dict(
                args=[[str(t)], dict(frame=dict(duration=0, redraw=True),
                                      transition=dict(duration=0), mode="immediate")],
                label=str(t), method="animate",
            )
            for t in range(n_time)
        ],
    )


def build_heatmap_figure(field: np.ndarray) -> go.Figure:
    """Static full-field heatmap: x=price level, y=time, color=skew."""
    fig = go.Figure(go.Heatmap(z=field, colorscale=COLORSCALES["Amber"], zmin=-1, zmax=1))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#000000",
        xaxis=dict(title="Price Level (proxy)", color=GREY,
                    tickfont=dict(family="Consolas, Courier New, monospace")),
        yaxis=dict(title="Time Step", color=GREY,
                    tickfont=dict(family="Consolas, Courier New, monospace")),
        height=300,
        margin=dict(l=40, r=20, t=20, b=40),
        font=dict(family="Consolas, Courier New, monospace"),
    )
    return fig