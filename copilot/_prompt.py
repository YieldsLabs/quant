system_prompt = """
You are an effective quantitative analysis assistant. Your job is to help interpret data, perform statistical analyses, technical analyses and provide insights based on numerical information.
"""
signal_risk_prompt = """
Analyze the risk level for an open {side} position within the {timeframe} timeframe using the provided candlestick data.
Input Data:
- Current Candlestick Data: {curr_bar}
- Previous Candlestick Data: {prev_bar}
Output Requirements:
1. Determine the risk level for the position. Choose from the following options:
   - NONE
   - LOW
   - MODERATE
   - HIGH
2. Recommend values for {side} position:
   - Take Profit (TP)
   - Stop Loss (SL)
Provide the result only in format:
RISK_LEVEL: [Risk Level], TP: [Take Profit Value], SL: [Stop Loss Value]
"""
signal_risk_pattern = (
    r"RISK_LEVEL: (NONE|LOW|MODERATE|HIGH), TP: ([\d.]+), SL: ([\d.]+)"
)
