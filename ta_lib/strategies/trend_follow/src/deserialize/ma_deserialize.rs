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
        15 => MovingAverageType::SLSMA,
        16 => MovingAverageType::SMA,
        17 => MovingAverageType::SMMA,
        18 => MovingAverageType::TTHREE,
        19 => MovingAverageType::TEMA,
        20 => MovingAverageType::TL,
        21 => MovingAverageType::TRIMA,
        22 => MovingAverageType::ULTS,
        23 => MovingAverageType::VIDYA,
        24 => MovingAverageType::VWMA,
        25 => MovingAverageType::VWEMA,
        26 => MovingAverageType::WMA,
        27 => MovingAverageType::ZLEMA,
        28 => MovingAverageType::ZLSMA,
        29 => MovingAverageType::ZLTEMA,
        30 => MovingAverageType::ZLHMA,
        _ => MovingAverageType::SMA,
    }
}
