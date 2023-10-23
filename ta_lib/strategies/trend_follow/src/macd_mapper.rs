use shared::MACDType;

pub fn map_to_macd(macd_type: usize) -> MACDType {
    match macd_type {
        1 => MACDType::MACD,
        _ => MACDType::MACD,
    }
}
