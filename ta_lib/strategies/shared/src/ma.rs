use base::prelude::*;
use core::prelude::*;
use trend::{
    alma, dema, ema, frama, gma, hma, kama, kjs, lsma, md, rmsma, sinwma, sma, smma, t3, tema, tma,
    vwma, wma, zlema, zlsma,
};

#[derive(Copy, Clone)]
pub enum MovingAverageType {
    ALMA,
    DEMA,
    EMA,
    FRAMA,
    GMA,
    HMA,
    KAMA,
    KJS,
    LSMA,
    MD,
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
    ZLSMA,
}

pub fn ma_indicator(ma: &MovingAverageType, data: &OHLCVSeries, period: usize) -> Series<f32> {
    match ma {
        MovingAverageType::ALMA => alma(&data.close, period, 0.85, 6.0),
        MovingAverageType::DEMA => dema(&data.close, period),
        MovingAverageType::EMA => ema(&data.close, period),
        MovingAverageType::FRAMA => frama(&data.high, &data.low, &data.close, period),
        MovingAverageType::GMA => gma(&data.close, period),
        MovingAverageType::HMA => hma(&data.close, period),
        MovingAverageType::KAMA => kama(&data.close, period),
        MovingAverageType::KJS => kjs(&data.high, &data.low, period),
        MovingAverageType::LSMA => lsma(&data.close, period),
        MovingAverageType::MD => md(&data.close, period),
        MovingAverageType::RMSMA => rmsma(&data.close, period),
        MovingAverageType::SINWMA => sinwma(&data.close, period),
        MovingAverageType::SMA => sma(&data.close, period),
        MovingAverageType::SMMA => smma(&data.close, period),
        MovingAverageType::TTHREE => t3(&data.close, period),
        MovingAverageType::TEMA => tema(&data.close, period),
        MovingAverageType::TMA => tma(&data.close, period),
        MovingAverageType::VWMA => vwma(&data.close, &data.volume, period),
        MovingAverageType::WMA => wma(&data.close, period),
        MovingAverageType::ZLEMA => zlema(&data.close, period),
        MovingAverageType::ZLSMA => zlsma(&data.close, period),
    }
}
