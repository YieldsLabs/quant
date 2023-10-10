use shared::TrendCandleType;

pub fn map_to_candle(candle: usize) -> TrendCandleType {
    match candle {
        1 => TrendCandleType::BOTTLE,
        2 => TrendCandleType::DOUBLE_TROUBLE,
        3 => TrendCandleType::GOLDEN,
        4 => TrendCandleType::H,
        5 => TrendCandleType::HEXAD,
        6 => TrendCandleType::HIKKAKE,
        7 => TrendCandleType::MARUBOZU,
        8 => TrendCandleType::MASTER_CANDLE,
        9 => TrendCandleType::QUINTUPLETS,
        10 => TrendCandleType::SLINGSHOT,
        11 => TrendCandleType::THREE_CANDLES,
        12 => TrendCandleType::THREE_METHODS,
        13 => TrendCandleType::TASUKI,
        _ => TrendCandleType::THREE_CANDLES,
    }
}
