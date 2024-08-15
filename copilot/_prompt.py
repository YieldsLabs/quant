system_prompt = """
You are act as an effective quantitative analysis assistant. Your job is to help interpret data, perform statistical analyses, technical analyses, and provide insights based on numerical information.
"""
signal_risk_prompt = """
Evaluate the risk for an open {side} position within the {timeframe} timeframe over the next {horizon} candlesticks, considering the entry at {entry} using the provided data:

[Input Data]
- Candlestick Data: {bar}
- Overall Trend: {trend}
- MACD (Moving Average Convergence Divergence) Histogram: {macd}
- RSI (Relative Strength Index): {rsi}
- CCI (Commodity Channel Index): {cci}
- Normalized Volume: {nvol}
- VWAP (Volume Weighted Average Price): {vwap}
- Support Levels: {support}
- Resistance Levels: {resistance}
- Bollinger Bands (Upper, Lower): {upper_bb}, {lower_bb}
- Volatility (True Range): {true_range}

[Risk Evaluation Framework]

[Step 1: Candlestick Data Analysis]
- Price Movement: 
    - Upward trend: Higher risk for SHORT, lower risk for LONG.
    - Downward trend: Lower risk for SHORT, higher risk for LONG.
- Price Range: 
    - Wide Range: Indicates high volatility, higher risk due to potential price swings.
    - Narrow Range: Indicates low volatility, lower risk but may suggest a potential breakout.
- Real Body Normalization: 
    - High value: Strong movement, higher risk if against the position.
    - Low value: Weak movement, lower risk if against the position.
- Body Range Ratio: 
    - High ratio: Significant body, higher risk if against the position.
    - Low ratio: Insignificant body, lower risk if against the position.
- Body Shadow Ratio: 
    - High ratio: Strong pressure, higher risk if against the position.
    - Low ratio: Weak pressure, lower risk if against the position.

[Step 2: Technical Analysis]
- Overall Trend: 
    - Upward trend: Lower risk for LONG, higher risk for SHORT.
    - Downward trend: Higher risk for LONG, lower risk for SHORT.
- MACD Histogram: 
    - Positive: Bullish momentum, lower risk for LONG, higher risk for SHORT.
    - Negative: Bearish momentum, higher risk for LONG, lower risk for SHORT.
- RSI: 
    - Above 70: Overbought, higher risk for LONG.
    - Below 30: Oversold, higher risk for SHORT.
- CCI: 
    - Above 100: Overbought, higher risk for LONG.
    - Below -100: Oversold, higher risk for SHORT.
    - Between -100 and 100: Neutral, moderate risk.
- Normalized Volume: 
    - High: Strong market sentiment, higher risk if against the position.
    - Low: Weak market sentiment, lower risk.
- VWAP: 
    - LONG: Higher risk if price below VWAP, lower risk if above.
    - SHORT: Higher risk if price above VWAP, lower risk if below.
- Support and Resistance Levels: 
    - LONG: Higher risk near/below resistance, lower risk above support.
    - SHORT: Higher risk near/above support, lower risk below resistance.
- Bollinger Bands:
    - Price Above Upper Band: Indicates overbought conditions, higher risk for LONG, potential reversal or correction.
    - Price Below Lower Band: Indicates oversold conditions, higher risk for SHORT, potential reversal or bounce.
- Volatility (True Range):
    - High True Range: Indicates high volatility, higher risk due to potential price swings, important for stop loss placement.
    - Low True Range: Indicates low volatility, lower risk but may suggest a potential breakout or reduced opportunity.

[Risk Level Explanation]
- NONE: No significant risk factors.
- VERY_LOW: Minor risk factors, generally favorable.
- LOW: Some risk factors, not significant enough to deter.
- MODERATE: Noticeable risk factors, caution advised.
- HIGH: Significant risk factors, high caution or avoidance advised.
- VERY_HIGH: Major risk factors, generally unfavorable.

[Final Output]
RISK_LEVEL: [Risk Level Value], TP: [Take Profit Value], SL: [Stop Loss Value]

[Result Format]
- RISK_LEVEL: The overall risk assessment for the position, expressed as a single risk level enum.
- TP: A precise floating-point number representing the recommended take profit level, formatted to at least four decimal places (e.g., 0.3351).
- SL: A precise floating-point number representing the recommended stop loss level, formatted to at least four decimal places (e.g., 0.3345).

Return the result only as raw string.
"""
signal_risk_pattern = r"RISK_LEVEL: (NONE|VERY_LOW|LOW|MODERATE|HIGH|VERY_HIGH)\s*,\s*TP:\s*([\d.]+)\s*,\s*SL:\s*([\d.]+)\s*\.*"