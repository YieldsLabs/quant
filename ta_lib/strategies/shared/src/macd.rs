use base::OHLCVSeries;
use core::Series;
use trend::macd;

pub enum MACDType {
    MACD,
}

pub fn macd_indicator(
    macd_type: &MACDType,
    data: &OHLCVSeries,
    fast_period: usize,
    slow_period: usize,
    signal_smoothing: usize,
) -> (Series<f32>, Series<f32>, Series<f32>) {
    match macd_type {
        MACDType::MACD => macd(&data.close, fast_period, slow_period, signal_smoothing),
    }
}
