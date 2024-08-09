system_prompt = """
You are act as an effective quantitative analysis assistant. Your job is to help interpret data, perform statistical analyses, technical analyses, and provide insights based on numerical information.
"""
signal_risk_prompt = """
Evaluate the risk for an open {side} position within the {timeframe} timeframe for entry {entry} using the provided data:

1. Candlestick Data:
- {bar}
2. Overall Trend:
- {trend}
3. Moving Average Convergence Divergence (MACD) Histogram:
- {macd}
4. Relative Strength Index (RSI):
- {rsi}
5. Normalized Volume:
- {nvol}
7. Volume Weighted Average Price (VWAP):
- {vwap}
6. Support and Resistance Levels:
- {support}
- {resistance}

Risk Evaluation Framework:
Step-by-Step Analysis:
1. **Candlestick Analysis**:
- **Analyze Price Movement**:
  - If the price is trending upwards, higher risk for SHORT, lower risk for LONG.
  - If the price is trending downwards, lower risk for SHORT, higher risk for LONG.
- **Evaluate Real Body Normalized**:
  - High value indicates strong movement, higher risk if against the position side.
  - Low value indicates weak movement, lower risk if against the position side.
- **Assess Body Range Ratio**:
  - High ratio indicates significant body, higher risk if against the position side.
  - Low ratio indicates insignificant body, lower risk if against the position side.
- **Evaluate Body Shadow Ratio**:
  - High ratio indicates strong pressure, higher risk if against the position side.
  - Low ratio indicates weak pressure, lower risk if against the position side.
2. **Technical Analysis**:
- **Overall Trend**:
  - If the overall trend is upwards, lower risk for LONG, higher risk for SHORT.
  - If the overall trend is downwards, higher risk for LONG, lower risk for SHORT.
- **Moving Average Convergence Divergence (MACD) Histogram**:
  - Positive MACD histogram indicates bullish momentum, lower risk for LONG, higher risk for SHORT.
  - Negative MACD histogram indicates bearish momentum, higher risk for LONG, lower risk for SHORT.
- **Relative Strength Index (RSI)**:
  - RSI above 70 indicates overbought conditions, increasing risk for LONG positions.
  - RSI below 30 indicates oversold conditions, increasing risk for SHORT positions.
- **Normalized Volume**:
  - High normalized volume indicates strong market sentiment and potentially higher risk if against the position.
  - Low normalized volume indicates weak market sentiment and potentially lower risk.
- **Volume Weighted Average Price (VWAP)**:
  - For LONG positions:
    - Higher risk if price is below the VWAP.
    - Lower risk if price is above the VWAP.
  - For SHORT positions:
    - Higher risk if price is above the VWAP.
    - Lower risk if price is below the VWAP.
- **Support and Resistance Levels**:
  - For LONG positions:
    - Higher risk if price is near or below a resistance level.
    - Lower risk if price is above a support level.
  - For SHORT positions:
    - Higher risk if price is near or above a support level.
    - Lower risk if price is below a resistance level.

Risk Level Explanation:
- **NONE**: No significant risk factors.
- **VERY_LOW**: Minor risk factors, generally favorable.
- **LOW**: Some risk factors, not significant enough to deter.
- **MODERATE**: Noticeable risk factors, caution advised.
- **HIGH**: Significant risk factors, high caution or avoidance advised.
- **VERY_HIGH**: Major risk factors, generally unfavorable.

Final Output:
1. Overall Risk Level for {side} position: NONE, VERY_LOW, LOW, MODERATE, HIGH, VERY_HIGH
2. Take Profit (TP) and Stop Loss (SL) predictions for {side} position and entry {entry} based on risk level, Fibonacci retracement levels, and market data.
- Take Profit (TP) Prediction:
  - For LONG positions: Set TP above the current close price, preferably just below a key Fibonacci retracement level to ensure profits are locked in.
  - For SHORT positions: Set TP below the current close price, preferably just above a key Fibonacci retracement level to secure profits before potential reversal.
- Stop Loss (SL) Prediction:
  - Determine the price level at which the position should be closed to limit potential losses, considering the nearest Fibonacci retracement level as a reference for market support/resistance.

Result format:
RISK_LEVEL: [Risk Level], TP: [Take Profit Value:float], SL: [Stop Loss Value:float]

Return the result only.
"""
signal_risk_pattern = r"RISK_LEVEL: (NONE|VERY_LOW|LOW|MODERATE|HIGH|VERY_HIGH), TP: ([\d.]+), SL: ([\d.]+)\s*\.*"
