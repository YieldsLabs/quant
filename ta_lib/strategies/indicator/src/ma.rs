use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use trend::{
    alma, cama, dema, ema, frama, gma, hema, hma, kama, lsma, md, midpoint, rmsma, sinwma, slsma,
    sma, smma, t3, tema, trima, ults, vidya, vwema, vwma, wma, zlema, zlhma, zlsma, zltema,
};

#[derive(Copy, Clone)]
pub enum MovingAverageType {
    ALMA,
    CAMA,
    DEMA,
    EMA,
    FRAMA,
    GMA,
    HMA,
    HEMA,
    KAMA,
    KJS,
    LSMA,
    MD,
    RMSMA,
    SINWMA,
    SLSMA,
    SMA,
    SMMA,
    TTHREE,
    TEMA,
    TL,
    TRIMA,
    ULTS,
    VIDYA,
    VWMA,
    VWEMA,
    WMA,
    ZLEMA,
    ZLSMA,
    ZLTEMA,
    ZLHMA,
}

pub fn ma_indicator(
    ma: &MovingAverageType,
    data: &OHLCVSeries,
    source: SourceType,
    period: usize,
) -> Series<f32> {
    let source = data.source(source);

    match ma {
        MovingAverageType::ALMA => alma(&source, period, 0.85, 6.0),
        MovingAverageType::CAMA => cama(&source, data.high(), data.low(), &data.wtr(), period),
        MovingAverageType::DEMA => dema(&source, period),
        MovingAverageType::EMA => ema(&source, period),
        MovingAverageType::FRAMA => frama(&source, data.high(), data.low(), period),
        MovingAverageType::GMA => gma(&source, period),
        MovingAverageType::HMA => hma(&source, period),
        MovingAverageType::HEMA => hema(&source, period),
        MovingAverageType::KAMA => kama(&source, period),
        MovingAverageType::KJS => midpoint(data.high(), data.low(), 26),
        MovingAverageType::LSMA => lsma(&source, period),
        MovingAverageType::MD => md(&source, period),
        MovingAverageType::RMSMA => rmsma(&source, period),
        MovingAverageType::SINWMA => sinwma(&source, period),
        MovingAverageType::SLSMA => slsma(&source, period),
        MovingAverageType::SMA => sma(&source, period),
        MovingAverageType::SMMA => smma(&source, period),
        MovingAverageType::TTHREE => t3(&source, period),
        MovingAverageType::TEMA => tema(&source, period),
        MovingAverageType::TL => midpoint(data.high(), data.low(), 55),
        MovingAverageType::TRIMA => trima(&source, period),
        MovingAverageType::ULTS => ults(&source, period),
        MovingAverageType::VIDYA => vidya(&source, period, 3 * period),
        MovingAverageType::VWMA => vwma(&source, data.volume(), period),
        MovingAverageType::VWEMA => vwema(&source, data.volume(), period),
        MovingAverageType::WMA => wma(&source, period),
        MovingAverageType::ZLEMA => zlema(&source, period),
        MovingAverageType::ZLSMA => zlsma(&source, period),
        MovingAverageType::ZLTEMA => zltema(&source, period),
        MovingAverageType::ZLHMA => zlhma(&source, period, 3),
    }
}
