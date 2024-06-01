system_prompt = """
You are an effective quantitative analysis assistant. Your job is to help interpret data, perform statistical analyses, technical analyses and provide insights based on numerical information.
"""
signal_risk_prompt = """
Evaluate the risk for an open {side} position in the {timeframe} timeframe using the following data:
1. Candlestick Data:
   - Previous Bar: {prev_bar}
   - Current Bar: {curr_bar}
2. Technical Indicators:
   - Moving Average Convergence/Divergence (MACD) Histogram: {macd_histogram}
   - Relative Strength Index (RSI): {rsi}
   - Bollinger Bands % (BB%): {bbp}
   - Stochastic Oscillator (K%): {k}
Framework for Risk Evaluation:
Step-by-Step Analysis:
1. **Candlestick Analysis**:
   - **Identify Candlestick Type**:
     - If the current candlestick is Bullish, the risk is higher for SHORT and lower for LONG.
     - If the current candlestick is Bearish, the risk is lower for SHORT and higher for LONG.
   - **Analyze Price Movement**:
     - If the price is moving upwards, the risk is higher for SHORT and lower for LONG.
     - If the price is moving downwards, the risk is lower for SHORT and higher for LONG.
   - **Evaluate Real Body Normalized**:
     - A high value indicates strong movement. This represents higher risk if against the position side.
     - A low value indicates weak movement. This represents lower risk if against the position side.
   - **Assess Body Range Ratio**:
     - A high ratio indicates a significant body. This represents higher risk if against the position side.
     - A low ratio indicates an insignificant body. This represents lower risk if against the position side.
   - **Calculate Body Shadow Ratio**:
     - A high ratio indicates strong pressure. This represents higher risk if against the position side.
     - A low ratio indicates weak pressure. This represents lower risk if against the position side.
2. **Technical Indicators Analysis**:
   - **Evaluate MACD Histogram**:
     - Positive and Increasing: Higher risk for SHORT, Lower risk for LONG.
     - Positive and Decreasing: Moderate risk for both sides.
     - Negative and Increasing: Moderate risk for both sides.
     - Negative and Decreasing: Lower risk for SHORT, Higher risk for LONG.
   - **Analyze RSI**:
     - Above 70: Higher risk for SHORT, Lower risk for LONG (overbought).
     - Between 30 and 70: Lower risk for both sides.
     - Below 30: Higher risk for LONG, Lower risk for SHORT (oversold).
   - **Assess BB%**:
     - Near 1: Higher risk for SHORT, Lower risk for LONG (upper band, overbought).
     - Near 0: Lower risk for SHORT, Higher risk for LONG (lower band, oversold).
   - **Evaluate Stochastic Oscillator (K%)**:
     - Above 80: Higher risk for SHORT, Lower risk for LONG (overbought).
     - Between 20 and 80: Lower risk for both sides.
     - Below 20: Higher risk for LONG, Lower risk for SHORT (oversold).
Risk Level Explanation:
- **NONE**: No significant risk factors present.
- **VERY_LOW**: Minor risk factors, generally favorable for position.
- **LOW**: Some risk factors, but not significant enough to deter position.
- **MODERATE**: Noticeable risk factors, caution advised.
- **HIGH**: Significant risk factors, high caution or avoidance advised.
- **VERY_HIGH**: Major risk factors, generally unfavorable for position.
Final Output:
1. Determine the overall Risk Level for {side} position based on the above analyses: NONE, VERY_LOW, LOW, MODERATE, HIGH, VERY_HIGH
2. Provide Take Profit (TP) and Stop Loss (SL) predictions for {side} position based on risk level and market data.
Result format:
RISK_LEVEL: [Risk Level], TP: [Take Profit Value], SL: [Stop Loss Value]
Return the result only.
"""
signal_risk_pattern = r"RISK_LEVEL: (NONE|LOW|VERY_LOW|LOW|MODERATE|HIGH|VERY_HIGH), TP: ([\d.]+), SL: ([\d.]+)"
