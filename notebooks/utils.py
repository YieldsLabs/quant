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
    return go.Candlestick(
        x=data['timestamp'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        increasing_line_color='green',
        decreasing_line_color='red' ,
        name="OHLC"
    )

def plot_candlestick(data: pd.DataFrame) -> go.Figure:
    n = len(data)
    rows = (n + 1) // 3
    cols = 3
    
    fig = make_subplots(
        rows=rows,
        cols=cols,
        shared_xaxes=False,
        subplot_titles=list(data.keys()),
        vertical_spacing=0.1,
    )

    row = 1
    col = 1
    
    for title, df in data.items():
        candlestick = create_candlestick(df)
        
        fig.add_trace(candlestick, row=row, col=col)
        
        if col == 3:
            col = 1
            row += 1
        else:
            col += 1

    fig.update_layout(
        showlegend=False,
        template='plotly_dark',
        height=320 * rows,
        width=1100,
        legend_orientation="h",
        plot_bgcolor='black',
        paper_bgcolor='black',
        margin=dict(
            autoexpand=False,
            l=40,
            r=15,
            t=60,
            b=40
        )
    )

    fig.update_xaxes(rangeslider_visible=False)
    return fig