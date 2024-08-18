system_prompt = """
You are act as an effective quantitative analysis assistant. Your job is to help interpret data, perform statistical analyses, technical analyses, and provide insights based on numerical information.
"""
signal_trend_risk_prompt = """
Evaluate the risk for an open {side} position within the {timeframe} timeframe over the next {horizon} candlesticks, considering the ENTRY PRICE at {entry} using the provided data:

[Input Data]
- Candlestick Data: {bar}
- Overall Trend (Exponential Moving Average): {trend}
- MACD (Moving Average Convergence/Divergence) Histogram: {macd}
- RSI (Relative Strength Index): {rsi}
- CCI (Commodity Channel Index): {cci}
- Normalized Volume: {nvol}
- VWAP (Volume Weighted Average Price): {vwap}
- Support/Resistance Levels: {support}/{resistance}
- Bollinger Bands (UPPER BAND, LOWER BAND): {upper_bb}, {lower_bb}
- Volatility (TRUE RANGE): {true_range}

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
- Support/Resistance Levels:
    - LONG: Higher risk near/below resistance, lower risk above support.
    - SHORT: Higher risk near/above support, lower risk below resistance.
- Bollinger Bands (UPPER BAND, LOWER BAND):
    - Price Above UPPER BAND: Indicates overbought conditions, higher risk for LONG, potential reversal or correction.
    - Price Below LOWER BAND: Indicates oversold conditions, higher risk for SHORT, potential reversal or bounce.
- Volatility (TRUE RANGE):
    - High TRUE RANGE: Indicates high volatility, higher risk due to potential price swings, important for stop loss placement.
    - Low TRUE RANGE: Indicates low volatility, lower risk but may suggest a potential breakout or reduced opportunity.

[Risk Level Explanation]
- NONE: No significant risk factors.
- VERY_LOW: Minor risk factors, generally favorable.
- LOW: Some risk factors, not significant enough to deter.
- MODERATE: Noticeable risk factors, caution advised.
- HIGH: Significant risk factors, high caution or avoidance advised.
- VERY_HIGH: Major risk factors, generally unfavorable.

[Final Output]
- **RISK_LEVEL**: [Risk Level Value]
- **TP**: [Take Profit Value] (formatted to six decimal places)
- **SL**: [Stop Loss Value] (formatted to six decimal places)

Return the result only as raw string:
RISK_LEVEL: [Risk Level Value], TP: [Take Profit Value], SL: [Stop Loss Value]
"""
signal_contrarian_risk_prompt = """
Evaluate the risk for an open {side} position within the {timeframe} timeframe over the next {horizon} candlesticks, considering the entry at {entry} using the provided data:

[Input Data]
- Candlestick Data: {bar}
- Overall Trend (Exponential Moving Average): {trend}
- MACD (Moving Average Convergence/Divergence) Histogram: {macd}
- RSI (Relative Strength Index): {rsi}
- CCI (Commodity Channel Index): {cci}
- Normalized Volume: {nvol}
- VWAP (Volume Weighted Average Price): {vwap}
- Support/Resistance Levels: {support} / {resistance}
- Bollinger Bands (UPPER BAND, LOWER BAND): {upper_bb}, {lower_bb}
- Volatility (TRUE RANGE): {true_range}

[Risk Evaluation Framework]

[Step 1: Candlestick Data Analysis]
- Price Movement:
    - Upward trend: Reversal risk higher for LONG, lower for SHORT.
    - Downward trend: Rebound risk higher for SHORT, lower for LONG.
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
- Overall Trend:
    - Upward: Higher reversal risk for LONG.
    - Downward: Higher rebound risk for SHORT.
- MACD Histogram:
    - Positive: Potential exhaustion.
    - Negative: Potential rebound.
- RSI:
    - Above 70: Overbought, reversal likely.
    - Below 30: Oversold, rebound likely.
- CCI:
    - Above 100: Overbought, reversal likely.
    - Below -100: Oversold, rebound likely.
- Normalized Volume:
    - High: Strong sentiment, potential exhaustion.
    - Low: Weak sentiment, potential reversal.
- VWAP:
    - LONG: Higher risk above VWAP.
    - SHORT: Higher risk below VWAP.
- Support and Resistance Levels:
    - LONG: Higher risk near resistance.
    - SHORT: Higher risk near support.
- Bollinger Bands (UPPER BAND, LOWER BAND):
    - Above UPPER BAND: Overbought, reversal risk for LONG.
    - Below LOWER BAND: Oversold, rebound risk for SHORT.
    - Bollinger Bands Width:
        - Wide (Significant gap between UPPER BAND and LOWER BAND): Indicates high volatility, potential breakout risk.
        - Narrow (Small gap between UPPER BAND and LOWER BAND): Indicates low volatility, potential for explosive movement if bands expand.
- Volatility (TRUE RANGE):
    - High: Higher reversal risk.
    - Low: Consolidation with lower risk.

[Risk Level Explanation]
- NONE: No significant risk factors.
- VERY_LOW: Minor risk factors, generally favorable.
- LOW: Some risk factors, not significant enough to deter.
- MODERATE: Noticeable risk factors, caution advised.
- HIGH: Significant risk factors, high caution or avoidance advised.
- VERY_HIGH: Major risk factors, generally unfavorable.

[Final Output]
- **RISK_LEVEL**: [Risk Level Value]
- **TP**: [Take Profit Value] (formatted to six decimal places)
- **SL**: [Stop Loss Value] (formatted to six decimal places)

Return the result only as raw string:
RISK_LEVEL: [Risk Level Value], TP: [Take Profit Value], SL: [Stop Loss Value]
"""
signal_risk_pattern = r"RISK_LEVEL:\s*(NONE|VERY_LOW|LOW|MODERATE|HIGH|VERY_HIGH)\s*,\s*TP:\s*([\d.]+)\s*,\s*SL:\s*([\d.]+)\s*\.*"
