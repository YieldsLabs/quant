use base::OHLCVSeries;
use core::Series;
use momentum::rsi;
use std::fmt;

pub enum RSIType {
    RSI,
}

impl fmt::Display for RSIType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::RSI => write!(f, "RSI"),
        }
    }
}

pub fn rsi_indicator(rsi_type: &RSIType, data: &OHLCVSeries, period: usize) -> Series<f32> {
    match rsi_type {
        RSIType::RSI => rsi(&data.close, period),
    }
}
