use base::OHLCVSeries;
use core::series::Series;
use std::fmt;
use trend::{
    alma, dema, ema, frama, gma, hma, kama, rmsma, sinwma, sma, smma, t3, tema, tma, vwma, wma,
    zlema,
};

pub enum MovingAverageType {
    ALMA,
    DEMA,
    EMA,
    FRAMA,
    GMA,
    HMA,
    KAMA,
    RMSMA,
    SINWMA,
    SMA,
    SMMA,
    TTHREE,
    TEMA,
    TMA,
    VWMA,
    WMA,
    ZLEMA,
}

impl fmt::Display for MovingAverageType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::ALMA => write!(f, "ALMA"),
            Self::DEMA => write!(f, "DEMA"),
            Self::EMA => write!(f, "EMA"),
            Self::FRAMA => write!(f, "FRAMA"),
            Self::GMA => write!(f, "GMA"),
            Self::HMA => write!(f, "HMA"),
            Self::KAMA => write!(f, "KAMA"),
            Self::RMSMA => write!(f, "RMSMA"),
            Self::SINWMA => write!(f, "SINWMA"),
            Self::SMA => write!(f, "SMA"),
            Self::SMMA => write!(f, "SMMA"),
            Self::TTHREE => write!(f, "T3"),
            Self::TEMA => write!(f, "TEMA"),
            Self::TMA => write!(f, "TMA"),
            Self::VWMA => write!(f, "VWMA"),
            Self::WMA => write!(f, "WMA"),
            Self::ZLEMA => write!(f, "ZLEMA"),
        }
    }
}

pub fn ma(smoothing: &MovingAverageType, data: &OHLCVSeries, period: usize) -> Series<f32> {
    match smoothing {
        MovingAverageType::ALMA => alma(&data.close, period, 0.85, 6.0),
        MovingAverageType::DEMA => dema(&data.close, period),
        MovingAverageType::EMA => ema(&data.close, period),
        MovingAverageType::FRAMA => frama(&data.high, &data.low, &data.close, period),
        MovingAverageType::GMA => gma(&data.close, period),
        MovingAverageType::HMA => hma(&data.close, period),
        MovingAverageType::KAMA => kama(&data.close, period),
        MovingAverageType::RMSMA => rmsma(&data.close, period),
        MovingAverageType::SINWMA => sinwma(&data.close, period),
        MovingAverageType::SMA => sma(&data.close, period),
        MovingAverageType::SMMA => smma(&data.close, period),
        MovingAverageType::TTHREE => t3(&data.close, period),
        MovingAverageType::TEMA => tema(&data.close, period),
        MovingAverageType::TMA => tma(&data.close, period),
        MovingAverageType::VWMA => vwma(&data.close, &data.volume, period),
        MovingAverageType::WMA => wma(&data.close, period),
        MovingAverageType::ZLEMA | _ => zlema(&data.close, period),
    }
}
