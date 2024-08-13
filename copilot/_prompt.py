system_prompt = """
You are act as an effective quantitative analysis assistant. Your job is to help interpret data, perform statistical analyses, technical analyses, and provide insights based on numerical information.
"""
signal_risk_prompt = """
Evaluate the risk for an open {side} position within the {timeframe} timeframe over the next {horizon} candlesticks, considering the entry at {entry} using the provided data:

### Input Data:
- **Candlestick Data**:
   - {bar}
- **Overall Trend**:
   - {trend}
- **MACD (Moving Average Convergence Divergence) Histogram**:
   - {macd}
- **RSI (Relative Strength Index)**:
   - {rsi}
- **CCI (Commodity Channel Index)**:
   - {cci}
- **Normalized Volume**:
   - {nvol}
- **VWAP (Volume Weighted Average Price)**:
   - {vwap}
- **Support and Resistance Levels**:
   - Support: {support}
   - Resistance: {resistance}

### Risk Evaluation Framework:

#### Step 1: Candlestick Data Analysis
- **Price Movement**:
  - Upward trend: Higher risk for SHORT, lower risk for LONG.
  - Downward trend: Lower risk for SHORT, higher risk for LONG.
- **Price Range**:
  - Wide Range: Indicates high volatility, higher risk due to potential price swings.
  - Narrow Range: Indicates low volatility, lower risk but may suggest a potential breakout.
- **Real Body Normalization**:
  - High value: Strong movement, higher risk if against the position.
  - Low value: Weak movement, lower risk if against the position.
- **Body Range Ratio**:
  - High ratio: Significant body, higher risk if against the position.
  - Low ratio: Insignificant body, lower risk if against the position.
- **Body Shadow Ratio**:
  - High ratio: Strong pressure, higher risk if against the position.
  - Low ratio: Weak pressure, lower risk if against the position.

#### Step 2: Technical Analysis
- **Overall Trend**:
  - Upward trend: Lower risk for LONG, higher risk for SHORT.
  - Downward trend: Higher risk for LONG, lower risk for SHORT.
- **MACD Histogram**:
  - Positive: Bullish momentum, lower risk for LONG, higher risk for SHORT.
  - Negative: Bearish momentum, higher risk for LONG, lower risk for SHORT.
- **RSI**:
  - Above 70: Overbought, higher risk for LONG.
  - Below 30: Oversold, higher risk for SHORT.
- **CCI**:
  - Above 100: Overbought, higher risk for LONG.
  - Below -100: Oversold, higher risk for SHORT.
  - Between -100 and 100: Neutral, moderate risk.
- **Normalized Volume**:
  - High: Strong market sentiment, higher risk if against the position.
  - Low: Weak market sentiment, lower risk.
- **VWAP**:
  - LONG: Higher risk if price below VWAP, lower risk if above.
  - SHORT: Higher risk if price above VWAP, lower risk if below.
- **Support and Resistance**:
  - LONG: Higher risk near/below resistance, lower risk above support.
  - SHORT: Higher risk near/above support, lower risk below resistance.

### Risk Level Explanation:
- **NONE**: No significant risk factors.
- **VERY_LOW**: Minor risk factors, generally favorable.
- **LOW**: Some risk factors, not significant enough to deter.
- **MODERATE**: Noticeable risk factors, caution advised.
- **HIGH**: Significant risk factors, high caution or avoidance advised.
- **VERY_HIGH**: Major risk factors, generally unfavorable.

### Final Output:
1. **Overall Risk Level** for {side} position: NONE, VERY_LOW, LOW, MODERATE, HIGH, VERY_HIGH
2. **Take Profit (TP) and Stop Loss (SL) Recommendations** based on risk level, Fibonacci retracement levels, and market data:
   - **Take Profit (TP)**:
     - LONG: Set TP above current close, ideally just below a key Fibonacci level.
     - SHORT: Set TP below current close, ideally just above a key Fibonacci level.
   - **Stop Loss (SL)**:
     - Determine SL based on nearest Fibonacci level to limit potential losses.

### Result Format:
RISK_LEVEL: [Risk Level Value], TP: [Take Profit Value], SL: [Stop Loss Value]
- **RISK_LEVEL**: The overall risk assessment for the position, expressed as a single risk level enum.
- **TP (Take Profit Value)**: A precise floating-point number representing the recommended take profit level, formatted to at least four decimal places (e.g., 0.3351).
- **SL (Stop Loss Value)**: A precise floating-point number representing the recommended stop loss level, formatted to at least four decimal places (e.g., 0.3345).

Return the result only.
"""
signal_risk_pattern = r"RISK_LEVEL: (NONE|VERY_LOW|LOW|MODERATE|HIGH|VERY_HIGH)\s*,\s*TP: ([\d.]+)\s*,\s*SL: ([\d.]+)\s*\.*"
