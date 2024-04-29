use base::prelude::*;
use core::prelude::*;
use trend::{
    alma, cama, dema, ema, frama, gma, hema, hma, kama, kjs, lsma, md, rmsma, sinwma, sma, smma,
    t3, tema, tma, vidya, vwema, vwma, wma, zlema, zlhma, zlsma, zltema,
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
    SMA,
    SMMA,
    TTHREE,
    TEMA,
    TMA,
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
    source_type: SourceType,
    period: usize,
) -> Series<f32> {
    match ma {
        MovingAverageType::ALMA => alma(&data.source(source_type), period, 0.85, 6.0),
        MovingAverageType::CAMA => cama(data.close(), data.high(), data.low(), &data.tr(), period),
        MovingAverageType::DEMA => dema(&data.source(source_type), period),
        MovingAverageType::EMA => ema(&data.source(source_type), period),
        MovingAverageType::FRAMA => frama(data.high(), data.low(), data.close(), period),
        MovingAverageType::GMA => gma(&data.source(source_type), period),
        MovingAverageType::HMA => hma(&data.source(source_type), period),
        MovingAverageType::HEMA => hema(&data.source(source_type), period),
        MovingAverageType::KAMA => kama(&data.source(source_type), period),
        MovingAverageType::KJS => kjs(data.high(), data.low(), period),
        MovingAverageType::LSMA => lsma(&data.source(source_type), period),
        MovingAverageType::MD => md(&data.source(source_type), period),
        MovingAverageType::RMSMA => rmsma(&data.source(source_type), period),
        MovingAverageType::SINWMA => sinwma(&data.source(source_type), period),
        MovingAverageType::SMA => sma(&data.source(source_type), period),
        MovingAverageType::SMMA => smma(&data.source(source_type), period),
        MovingAverageType::TTHREE => t3(&data.source(source_type), period),
        MovingAverageType::TEMA => tema(&data.source(source_type), period),
        MovingAverageType::TMA => tma(&data.source(source_type), period),
        MovingAverageType::VIDYA => vidya(&data.source(source_type), period, 3 * period),
        MovingAverageType::VWMA => vwma(&data.source(source_type), data.volume(), period),
        MovingAverageType::VWEMA => vwema(&data.source(source_type), data.volume(), period),
        MovingAverageType::WMA => wma(&data.source(source_type), period),
        MovingAverageType::ZLEMA => zlema(&data.source(source_type), period),
        MovingAverageType::ZLSMA => zlsma(&data.source(source_type), period),
        MovingAverageType::ZLTEMA => zltema(&data.source(source_type), period),
        MovingAverageType::ZLHMA => zlhma(&data.source(source_type), period, 3),
    }
}
