use shared::MovingAverageType;

pub fn map_to_ma(smoothing: usize) -> MovingAverageType {
    match smoothing {
        1 => MovingAverageType::ALMA,
        2 => MovingAverageType::DEMA,
        3 => MovingAverageType::EMA,
        4 => MovingAverageType::FRAMA,
        5 => MovingAverageType::GMA,
        6 => MovingAverageType::HMA,
        7 => MovingAverageType::KAMA,
        8 => MovingAverageType::KJS,
        9 => MovingAverageType::LSMA,
        10 => MovingAverageType::MD,
        11 => MovingAverageType::RMSMA,
        12 => MovingAverageType::SINWMA,
        13 => MovingAverageType::SMA,
        14 => MovingAverageType::SMMA,
        15 => MovingAverageType::TTHREE,
        16 => MovingAverageType::TEMA,
        17 => MovingAverageType::TMA,
        18 => MovingAverageType::VIDYA,
        19 => MovingAverageType::VWMA,
        20 => MovingAverageType::VWEMA,
        21 => MovingAverageType::WMA,
        22 => MovingAverageType::ZLEMA,
        23 => MovingAverageType::ZLSMA,
        24 => MovingAverageType::ZLTEMA,
        25 => MovingAverageType::ZLHMA,
        _ => MovingAverageType::SMA,
    }
}
