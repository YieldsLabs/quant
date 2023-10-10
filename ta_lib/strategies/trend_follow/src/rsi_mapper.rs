use shared::RSIType;

pub fn map_to_rsi(rsi_type: usize) -> RSIType {
    match rsi_type {
        1 => RSIType::RSI,
        _ => RSIType::RSI,
    }
}
