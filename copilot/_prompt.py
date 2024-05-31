system_prompt = """
You are an effective quantitative analysis assistant. Your job is to help interpret data, perform statistical analyses, technical analyses and provide insights based on numerical information.
"""
signal_risk_prompt = """
Analyze risk for an open {side} position in {timeframe} using provided candlestick data:
   - {curr_bar}
   - {prev_bar}
Output:
   1. Risk level: NONE, LOW, MODERATE, HIGH
   2. Recommendations for {side} position:
      - Take Profit (TP)
      - Stop Loss (SL)
Result format:
   RISK_LEVEL: [Risk Level], TP: [Take Profit Value], SL: [Stop Loss Value]
Return result only.
"""
signal_risk_pattern = (
    r"RISK_LEVEL: (NONE|LOW|MODERATE|HIGH), TP: ([\d.]+), SL: ([\d.]+)"
)
