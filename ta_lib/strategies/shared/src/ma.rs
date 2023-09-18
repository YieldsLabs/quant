use base::OHLCVSeries;
use core::series::Series;
use trend::{
    alma, dema, ema, frama, gma, hma, kama, rmsma, sinwma, sma, smma, t3, tema, tma, vwma, wma,
    zlema,
};

pub fn ma(smothing: &str, data: &OHLCVSeries, period: usize) -> Series<f32> {
    match smothing {
        "ALMA" => alma(&data.close, period, 0.85, 6.0),
        "DEMA" => dema(&data.close, period),
        "EMA" => ema(&data.close, period),
        "FRAMA" => frama(&data.high, &data.low, &data.close, period),
        "GMA" => gma(&data.close, period),
        "HMA" => hma(&data.close, period),
        "KAMA" => kama(&data.close, period),
        "RMSMA" => rmsma(&data.close, period),
        "SINWMA" => sinwma(&data.close, period),
        "SMA" => sma(&data.close, period),
        "SMMA" => smma(&data.close, period),
        "T3" => t3(&data.close, period),
        "TEMA" => tema(&data.close, period),
        "TMA" => tma(&data.close, period),
        "VWMA" => vwma(&data.close, &data.volume, period),
        "WMA" => wma(&data.close, period),
        "ZLEMA" | _ => zlema(&data.close, period),
    }
}
