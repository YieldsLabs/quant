system_prompt = """
You are act as an effective quantitative analysis assistant. Your job is to help interpret data, perform statistical analyses, technical analyses, forecast trend and provide insights based on numerical information.
"""
risk_intro = """
[Position Risk Evaluation Framework]

[Position Details]
- Side: {side}
- Timeframe: {timeframe}
- Horizon: Next {horizon} Candlesticks
- Entry Price: {entry}
- Strategy Type: {strategy_type}
"""
risk_outro = """
[Final Output]
- RL: [Risk Level Value:ENUM]
- TP: [Take Profit Value:.6f]
- SL: [Stop Loss Value:.6f]

[Example]
RL: MODERATE, TP: 7.4499, SL: 8.444

Return the result as raw string only.
"""
risk_data = """
[Input Data]
- Candlestick Data: {bar}
- EMA (Exponential Moving Average): {trend}
- MACD (Moving Average Convergence/Divergence) Histogram: {macd}
- RSI (Relative Strength Index): {rsi}
- CCI (Commodity Channel Index): {cci}
- ROC (Rate of Change): {roc}
- Normalized Volume: {nvol}
- VWAP (Volume Weighted Average Price): {vwap}
- Support/Resistance Levels:
    - Support: {support}
    - Resistance: {resistance}
- Bollinger Bands:
    - Upper: {upper_bb}
    - Lower: {lower_bb}
- Volatility (True Range): {true_range}
"""
trend_risk_framework = """
[Input Data Analysis]

[Step 1: Candlestick Data Analysis]
- Price Movement:
    - Upward: Higher risk for SHORT, lower risk for LONG.
    - Downward: Lower risk for SHORT, higher risk for LONG.
- Price Range:
    - Wide: Higher risk due to potential price swings.
    - Narrow: Lower risk but may suggest a potential breakout.
- Real Body Normalization:
    - High: Strong movement, higher risk if against the position.
    - Low: Weak movement, lower risk if against the position.
- Body Range Ratio:
    - High: Higher risk if against the position.
    - Low: Lower risk if against the position.
- Body Shadow Ratio:
    - High: Higher risk if against the position.
    - Low: Lower risk if against the position.

[Step 2: Technical Analysis]
- EMA:
    - Upward: Lower risk for LONG, higher risk for SHORT.
    - Downward: Higher risk for LONG, lower risk for SHORT.
- MACD Histogram:
    - Positive: Bullish momentum, lower risk for LONG, higher risk for SHORT.
    - Negative: Bearish momentum, higher risk for LONG, lower risk for SHORT.
- RSI:
    - Above 70: Overbought, higher risk for LONG.
    - Below 30: Oversold, higher risk for SHORT.
    - Between 30 and 70: Neutral, moderate risk for LONG and SHORT.
- CCI:
    - Above 100: Overbought, higher risk for LONG.
    - Below -100: Oversold, higher risk for SHORT.
    - Between -100 and 100: Neutral, moderate risk for LONG and SHORT.
- ROC:
    - Positive: Lower risk for LONG, higher risk for SHORT.
    - Negative: Higher risk for LONG, lower risk for SHORT.
- Normalized Volume:
    - High: Higher risk if against the position.
    - Low: Lower risk.
- VWAP:
    - Above: Favorable for LONG, increased risk for SHORT.
    - Below: Favorable for SHORT, increased risk for LONG.
- Support/Resistance Levels:
    - Near Resistance: Increased risk for LONG, favorable for SHORT.
    - Near Support: Favorable for LONG, increased risk for SHORT.
- Bollinger Bands:
    - Above Upper: Higher risk for LONG, potential reversal or correction.
    - Below Lower: Higher risk for SHORT, potential reversal or bounce.
- Volatility (True Range):
    - High: Higher risk due to potential price swings, tighter stops recommended for both LONG and SHORT.
    - Low: Suggests consolidation, with increased breakout potential, adjust risk management accordingly.
"""
contrarian_risk_framework = """
[Input Data Analysis]

[Step 1: Candlestick Data Analysis]
- Price Movement:
    - Upward: Reversal risk higher for LONG, lower for SHORT.
    - Downward: Rebound risk higher for SHORT, lower for LONG.
- Price Range:
    - Wide: Higher reversal risk if aligned with the trend.
    - Narrow: Consolidation with potential reversal or breakout.
- Real Body Normalization:
    - High: Strong trend, potential exhaustion.
    - Low: Weak trend, potential reversal.
- Body Range Ratio:
    - High: Significant movement, potential exhaustion.
    - Low: Insignificant movement, potential reversal.
- Body Shadow Ratio:
    - High: Pressure with potential reversal.
    - Low: Weak pressure, lower reversal risk.

[Step 2: Technical Analysis]
- EMA:
    - Upward: Indicates an overall upward trend, reducing risk for LONG and increasing risk for SHORT.
    - Downward: Suggests trend reversal, favorable for SHORT and riskier for LONG.
- MACD Histogram:
    - Positive: Potential exhaustion.
    - Negative: Potential rebound.
- RSI:
    - Above 70: Overbought, increased risk for LONG, favorable for SHORT.
    - Below 30: Oversold, favorable for LONG, increased risk for SHORT.
- CCI:
    - Above 100: Overbought, increased risk for LONG, favorable for SHORT.
    - Below -100: Oversold, favorable for LONG, increased risk for SHORT.
- ROC:
    - Positive: Potential exhaustion if combined with overbought signals, higher reversal risk.
    - Negative: Potential rebound if combined with oversold signals, higher rebound risk.
- Normalized Volume:
    - High: Strong sentiment, potential exhaustion.
    - Low: Weak sentiment, potential reversal.
- VWAP:
    - Above: Favorable for LONG, increased risk for SHORT.
    - Below: Favorable for SHORT, increased risk for LONG.
- Support/Resistance Levels:
    - Near Resistance: Increased risk for LONG, favorable for SHORT.
    - Near Support: Favorable for LONG, increased risk for SHORT.
- Bollinger Bands:
    - Above Upper: Overbought, reversal risk for LONG.
    - Below Lower: Oversold, rebound risk for SHORT.
    - Wide (Significant gap between Upper and Lower): Indicates high volatility, potential breakout risk.
    - Narrow (Small gap between Upper and Lower): Indicates low volatility, potential for explosive movement if bands expand.
- Volatility (True Range):
    - High: Indicates increased risk of sharp movements; tighter stops recommended for both LONG and SHORT.
    - Low: Suggests consolidation, with increased breakout potential, adjust risk management accordingly.
"""
risk_eval = """
[Step 3: Risk Level Management]
- NONE: No significant risk factors.
- VERY_LOW: Minor risk factors, generally favorable.
- LOW: Some risk factors, not significant enough to deter.
- MODERATE: Noticeable risk factors, caution advised.
- HIGH: Significant risk factors, high caution or avoidance advised.
- VERY_HIGH: Major risk factors, generally unfavorable.
"""
signal_trend_risk_prompt = f"{risk_intro}{risk_data}{trend_risk_framework}{risk_eval}{risk_outro}"
signal_contrarian_risk_prompt = f"{risk_intro}{risk_data}{contrarian_risk_framework}{risk_eval}{risk_outro}"
signal_risk_pattern = r"RL:\s*(NONE|VERY_LOW|LOW|MODERATE|HIGH|VERY_HIGH)\s*,\s*TP:\s*([\d.]+)\s*,\s*SL:\s*([\d.]+)\s*\.*"
