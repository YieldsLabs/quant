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
        8 => MovingAverageType::LSMA,
        9 => MovingAverageType::MD,
        10 => MovingAverageType::RMSMA,
        11 => MovingAverageType::SINWMA,
        12 => MovingAverageType::SMA,
        13 => MovingAverageType::SMMA,
        14 => MovingAverageType::TTHREE,
        15 => MovingAverageType::TEMA,
        16 => MovingAverageType::TMA,
        17 => MovingAverageType::VWMA,
        18 => MovingAverageType::WMA,
        19 => MovingAverageType::ZLEMA,
        20 => MovingAverageType::ZLSMA,
        _ => MovingAverageType::SMA,
    }
}
