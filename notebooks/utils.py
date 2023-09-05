import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_candlestick(data: pd.DataFrame) -> go.Figure:
    buy_color = 'cyan'  
    sell_color = 'magenta'

    stop_loss_color = 'red'
    take_profit_color = 'green'
    entry_color_long = 'limegreen'
    entry_color_short = 'darkred'
    exit_color_profit = 'green'
    exit_color_loss = 'red'

    increasing_color = 'lime'
    decreasing_color = 'orange'

    traces = []
    
    traces.append(
        go.Candlestick(
            x=data['timestamp'],
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            increasing_line_color=increasing_color,
            decreasing_line_color=decreasing_color,
            increasing_fillcolor=increasing_color,
            decreasing_fillcolor=decreasing_color,
            name="OHLC"
        )
    )

    traces.append(
        go.Scatter(
            x=data.loc[data['signal.side'] == 'BUY', 'timestamp'],
            y=data.loc[data['signal.side'] == 'BUY', 'close'],
            mode='markers',
            marker=dict(symbol='cross', size=8, color=buy_color),
            name='Buy'
        )
    )

    traces.append(
        go.Scatter(
            x=data.loc[data['signal.side'] == 'SELL', 'timestamp'],
            y=data.loc[data['signal.side'] == 'SELL', 'close'],
            mode='markers',
            marker=dict(symbol='cross', size=8, color=sell_color),
            name='Sell'
        )
    )


    traces.append(
        go.Scatter(
            x=data.loc[data['position.side'] == 'long', 'timestamp'],
            y=data.loc[data['position.side'] == 'long', 'position.entry_price'],
            mode='markers',
            marker=dict(symbol='triangle-up', size=12, color=entry_color_long),
            name='Long Entry'
        )
    )

    traces.append(
        go.Scatter(
            x=data.loc[data['position.side'] == 'short', 'timestamp'],
            y=data.loc[data['position.side'] == 'short', 'position.entry_price'],
            mode='markers',
            marker=dict(symbol='triangle-down', size=12, color=entry_color_short),
            name='Short Entry'
        )
    )


    return traces


def plot_candlestick(data: pd.DataFrame, charts_per_row: int = 2) -> go.Figure:
    n = len(data)
    rows = -(-n // charts_per_row)

    subplot_titles_list = [f"{key[0]} - {key[1]}" for key in data.keys()]
    
    fig = make_subplots(
        rows=rows,
        cols=charts_per_row,
        shared_xaxes=False,
        subplot_titles=subplot_titles_list,
    )

    row = 1
    col = 1
    
    for title, df in data.items():
        traces = create_candlestick(df)
        
        for trace in traces:
            fig.add_trace(trace, row=row, col=col)
        
        if col == charts_per_row:
            col = 1
            row += 1
        else:
            col += 1

    fig.update_layout(
        showlegend=False,
        template='plotly_dark',
        height=640 * rows,
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

def plot_equity_curve(df, symbol, timeframe, strategy):
    equity_curve = df['performance.equity'].iloc[-1]
    account_size = df['performance.account_size'].iloc[-1]
    drawdowns = df['performance.drawdown'].iloc[-1]
    sterling_ratio = df['performance.sterling_ratio'].iloc[-1]
    hit_ratio = df['performance.hit_ratio'].iloc[-1]
    total_pnl = df['performance.total_pnl'].iloc[-1]
    max_drawdown = df['performance.max_drawdown'].iloc[-1]
    max_runup = df['performance.max_runup'].iloc[-1]
    total_trades = df['performance.total_trades'].iloc[-1]
    profit_factor = df['performance.profit_factor'].iloc[-1]
    max_consecutive_wins = df['performance.max_consecutive_wins'].iloc[-1]
    max_consecutive_losses = df['performance.max_consecutive_losses'].iloc[-1]

    trades = list(range(1, total_trades + 1))

    color_above_account = 'teal'
    color_below_account = 'coral'

    def add_equity_curve_segment(fig, x, y, color):
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode='lines',
                line=dict(color=color, width=2),
                hoverinfo='y',
                showlegend=False
            )
        )

    fig = go.Figure()

    start_idx = 0
    current_color = color_above_account if equity_curve[0] >= account_size else color_below_account

    for idx, equity in enumerate(equity_curve[1:], 1):
        color = color_above_account if equity >= account_size else color_below_account
        if color != current_color:
            add_equity_curve_segment(fig, trades[start_idx:idx+1], equity_curve[start_idx:idx+1], current_color)
            start_idx = idx
            current_color = color

    add_equity_curve_segment(fig, trades[start_idx:], equity_curve[start_idx:], current_color)

    fig.add_trace(
        go.Bar(
            x=trades,
            y=[-drawdown * account_size for drawdown in drawdowns],
            orientation='v',
            marker_color='pink',
            yaxis='y2',
            opacity=0.4
        )
    )

    annotations0 = [
        f"Net Profit: ${total_pnl:.2f}",
        f"Hit Ratio: {hit_ratio:.2%}",
        f"Profit Factor: {profit_factor:.2f}",
        f"Max Drawdown: ${(account_size * max_drawdown):.2f}",
    ]


    y0_pos = 1.06
    spacing = 0.3

    for idx, annotation in enumerate(annotations0):
        fig.add_annotation(
            go.layout.Annotation(
                text=annotation,
                xref="paper", yref="paper",
                x=idx * spacing, y=y0_pos,
                showarrow=False,
                font=dict(size=12)
            )
        )

    annotations1 = [
        f"Max Consecutive Wins: {max_consecutive_wins}",
        f"Max Consecutive Losses: {max_consecutive_losses}",
        f"Sterling Ratio: {(sterling_ratio):.2f}",
        f"Max Runup: ${(account_size * max_runup):.2f}",
    ]


    y1_pos = 1.01
    spacing = 0.3

    for idx, annotation in enumerate(annotations1):
        fig.add_annotation(
            go.layout.Annotation(
                text=annotation,
                xref="paper", yref="paper",
                x=idx * spacing, y=y1_pos,
                showarrow=False,
                font=dict(size=12)
            )
        )

    fig.update_layout(
        title=f'{symbol} {timeframe} {strategy}',
        xaxis_rangeslider_visible=False,
        template='plotly_dark',
        showlegend=False,
        margin=dict(
            autoexpand=False,
            l=60,
            r=15,
            t=70,
            b=40
        ),
        xaxis=dict(
            title='',
            showgrid=False
        ),
        yaxis=dict(
            title="",
            showgrid=False
        ),
        yaxis2=dict(
            title="",
            overlaying='y',
            side='right',
            showgrid=False,
            showticklabels=False 
        )
    )

    return fig