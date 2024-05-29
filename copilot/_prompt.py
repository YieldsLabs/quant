system_prompt = """
You are an effective quantitative analysis assistant. Your job is to help interpret data, perform statistical analyses, technical analyses and provide insights based on numerical information.
"""
signal_risk_prompt = """
Candlestick data provided: {bar}
Make a decision about Risk Level for an open {side} position based on the candlestick data. Choose from: NONE, LOW, MODERATE, or HIGH.
Return only the decision about the Risk Level.
"""
