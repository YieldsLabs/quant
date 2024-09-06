use indicator::{CandleReversalType, CandleTrendType};

#[inline]
pub fn candletrend_deserialize(candle: usize) -> CandleTrendType {
    match candle {
        1 => CandleTrendType::BOTTLE,
        2 => CandleTrendType::DOUBLE_TROUBLE,
        3 => CandleTrendType::GOLDEN,
        4 => CandleTrendType::H,
        5 => CandleTrendType::HEXAD,
        6 => CandleTrendType::HIKKAKE,
        7 => CandleTrendType::MARUBOZU,
        8 => CandleTrendType::MASTER_CANDLE,
        9 => CandleTrendType::QUINTUPLETS,
        10 => CandleTrendType::SLINGSHOT,
        11 => CandleTrendType::THREE_CANDLES,
        12 => CandleTrendType::THREE_METHODS,
        13 => CandleTrendType::TASUKI,
        14 => CandleTrendType::THREE_ONE_TWO,
        _ => CandleTrendType::THREE_CANDLES,
    }
}

#[inline]
pub fn candlereversal_deserialize(candle: usize) -> CandleReversalType {
    match candle {
        1 => CandleReversalType::DOJI,
        2 => CandleReversalType::ENGULFING,
        3 => CandleReversalType::EUPHORIA,
        4 => CandleReversalType::HAMMER,
        5 => CandleReversalType::HARAMIF,
        6 => CandleReversalType::HARAMIS,
        7 => CandleReversalType::KANGAROO,
        8 => CandleReversalType::R,
        9 => CandleReversalType::SPLIT,
        10 => CandleReversalType::TWEEZERS,
        _ => CandleReversalType::R,
    }
}
