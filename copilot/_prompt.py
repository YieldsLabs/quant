system_prompt = """
You are an effective quantitative analysis assistant. Your job is to help interpret data, perform statistical analyses, technical analyses and provide insights based on numerical information.
"""
signal_risk_prompt = """
Evaluate the risk for an open {side} position within the {timeframe} timeframe using the provided data:

1. Candlestick Data:
- {bar}

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

2. **Anomaly Detection**:
- **Identify Price Anomalies**:
  - Significant deviation from normal patterns: Higher risk for both sides.
  - No significant deviation: Lower risk for both sides.

3. **Pattern Detection**:
- Identify and evaluate any one or two candlestick patterns that may impact the risk level

4. **Fibonacci Retracement Analysis**:
- **Identify Key Levels**:
  - Calculate Fibonacci retracement levels (23.6%, 38.2%, 50%, 61.8%, 78.6%) based on recent high and low prices.
- **Evaluate Position Relative to Fibonacci Levels**:
  - For LONG positions:
    - Higher risk if price is near or below a retracement level indicating potential resistance.
    - Lower risk if price is above a retracement level indicating potential support.
  - For SHORT positions:
    - Higher risk if price is near or above a retracement level indicating potential support.
    - Lower risk if price is below a retracement level indicating potential resistance.

5. **Volume Analysis**:
- **Evaluate Trading Volume**:
  - High volume during price moves can indicate strong market sentiment and potentially higher risk if against the position.
  - Low volume during price moves can indicate weak market sentiment and potentially lower risk.

Risk Level Explanation:
- **NONE**: No significant risk factors.
- **VERY_LOW**: Minor risk factors, generally favorable.
- **LOW**: Some risk factors, not significant enough to deter.
- **MODERATE**: Noticeable risk factors, caution advised.
- **HIGH**: Significant risk factors, high caution or avoidance advised.
- **VERY_HIGH**: Major risk factors, generally unfavorable.

Final Output:
1. Overall Risk Level for {side} position: NONE, VERY_LOW, LOW, MODERATE, HIGH, VERY_HIGH
2. Take Profit (TP) and Stop Loss (SL) predictions for {side} position based on risk level, Fibonacci retracement levels, and market data.
- Take Profit (TP) Prediction:
  - For LONG positions: Set TP above the current close price, preferably just below a key Fibonacci retracement level to ensure profits are locked in.
  - For SHORT positions: Set TP below the current close price, preferably just above a key Fibonacci retracement level to secure profits before potential reversal.
- Stop Loss (SL) Prediction:
  - Determine the price level at which the position should be closed to limit potential losses, considering the nearest Fibonacci retracement level as a reference for market support/resistance.

Result format:
RISK_LEVEL: [Risk Level], TP: [Take Profit Value], SL: [Stop Loss Value]

Return the result only.
"""
signal_risk_pattern = r"RISK_LEVEL: (NONE|LOW|VERY_LOW|LOW|MODERATE|HIGH|VERY_HIGH), TP: ([\d.]+), SL: ([\d.]+)"
