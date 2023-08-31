import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_candlestick(data: pd.DataFrame) -> go.Figure:
    return go.Candlestick(
        x=data['timestamp'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close']
    )

def create_candlestick(data: pd.DataFrame) -> go.Figure:
    return go.Figure(go.Candlestick(
        x=data['timestamp'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close']
    ))

def plot_candlestick(title: str, data: pd.DataFrame) -> go.Figure:
    fig = create_candlestick(data)

    fig.update_layout(
        title=title,
        xaxis_rangeslider_visible=False,
        height=600,
        width=1200
    )
    return fig