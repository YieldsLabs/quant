use shared::MovingAverageType;

pub fn map_to_ma(smoothing: usize) -> MovingAverageType {
    match smoothing {
        1 => MovingAverageType::ALMA,
        2 => MovingAverageType::DEMA,
        3 => MovingAverageType::CAMA,
        4 => MovingAverageType::EMA,
        5 => MovingAverageType::FRAMA,
        6 => MovingAverageType::GMA,
        7 => MovingAverageType::HMA,
        8 => MovingAverageType::KAMA,
        9 => MovingAverageType::KJS,
        10 => MovingAverageType::LSMA,
        11 => MovingAverageType::MD,
        12 => MovingAverageType::RMSMA,
        13 => MovingAverageType::SINWMA,
        14 => MovingAverageType::SMA,
        15 => MovingAverageType::SMMA,
        16 => MovingAverageType::TTHREE,
        17 => MovingAverageType::TEMA,
        18 => MovingAverageType::TMA,
        19 => MovingAverageType::VIDYA,
        20 => MovingAverageType::VWMA,
        21 => MovingAverageType::VWEMA,
        22 => MovingAverageType::WMA,
        23 => MovingAverageType::ZLEMA,
        24 => MovingAverageType::ZLSMA,
        25 => MovingAverageType::ZLTEMA,
        26 => MovingAverageType::ZLHMA,
        _ => MovingAverageType::SMA,
    }
}
