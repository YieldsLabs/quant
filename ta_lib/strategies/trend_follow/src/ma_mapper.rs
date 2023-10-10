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
        9 => MovingAverageType::RMSMA,
        10 => MovingAverageType::SINWMA,
        11 => MovingAverageType::SMA,
        12 => MovingAverageType::SMMA,
        13 => MovingAverageType::TTHREE,
        14 => MovingAverageType::TEMA,
        15 => MovingAverageType::TMA,
        16 => MovingAverageType::VWMA,
        17 => MovingAverageType::WMA,
        18 => MovingAverageType::ZLEMA,
        19 => MovingAverageType::ZLSMA,
        _ => MovingAverageType::SMA,
    }
}
