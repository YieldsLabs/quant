use indicator::MovingAverageType;

#[inline]
pub fn ma_deserialize(ma: usize) -> MovingAverageType {
    match ma {
        1 => MovingAverageType::ALMA,
        2 => MovingAverageType::DEMA,
        3 => MovingAverageType::CAMA,
        4 => MovingAverageType::EMA,
        5 => MovingAverageType::FRAMA,
        6 => MovingAverageType::GMA,
        7 => MovingAverageType::HMA,
        8 => MovingAverageType::HEMA,
        9 => MovingAverageType::KAMA,
        10 => MovingAverageType::KJS,
        11 => MovingAverageType::LSMA,
        12 => MovingAverageType::MD,
        13 => MovingAverageType::RMSMA,
        14 => MovingAverageType::SINWMA,
        15 => MovingAverageType::SMA,
        16 => MovingAverageType::SMMA,
        17 => MovingAverageType::TTHREE,
        18 => MovingAverageType::TEMA,
        19 => MovingAverageType::TRIMA,
        20 => MovingAverageType::VIDYA,
        21 => MovingAverageType::VWMA,
        22 => MovingAverageType::VWEMA,
        23 => MovingAverageType::WMA,
        24 => MovingAverageType::ZLEMA,
        25 => MovingAverageType::ZLSMA,
        26 => MovingAverageType::ZLTEMA,
        27 => MovingAverageType::ZLHMA,
        _ => MovingAverageType::SMA,
    }
}
