system_prompt = """
You are an effective quantitative analysis assistant. Your job is to help interpret data, perform statistical analyses, technical analyses and provide insights based on numerical information.
"""
signal_risk_prompt = """
Given the current candlestick data: {current_bar}, analyze the risk level for an open {side} position.
Options for risk level: NONE, LOW, MODERATE or HIGH.
Provide only the decision regarding the risk level.
"""
