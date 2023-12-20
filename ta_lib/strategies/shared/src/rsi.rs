use base::OHLCVSeries;
use core::prelude::*;
use momentum::rsi;

pub enum RSIType {
    RSI,
}

pub fn rsi_indicator(rsi_type: &RSIType, data: &OHLCVSeries, period: usize) -> Series<f32> {
    match rsi_type {
        RSIType::RSI => rsi(&data.close, period),
    }
}
