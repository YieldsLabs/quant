use base::{Filter, OHLCVSeries};
use core::Series;
use shared::{rsi_indicator, RSIType};

const RSI_NEUTRALITY: f32 = 50.0;
const RSI_UPPER_BOUND: f32 = 75.0;
const RSI_LOWER_BOUND: f32 = 25.0;

pub struct RSIFilter {
    rsi_type: RSIType,
    period: usize,
    threshold: f32,
}

impl RSIFilter {
    pub fn new(rsi_type: RSIType, period: f32, threshold: f32) -> Self {
        Self {
            rsi_type,
            period: period as usize,
            threshold,
        }
    }
}

impl Filter for RSIFilter {
    fn lookback(&self) -> usize {
        self.period
    }

    fn confirm(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi_indicator(&self.rsi_type, data, self.period);

        (
            rsi.sgte(RSI_NEUTRALITY)
                & rsi.slte(RSI_UPPER_BOUND)
                & rsi.shift(1).sgte(RSI_NEUTRALITY - self.threshold)
                & rsi.shift(2).sgte(RSI_NEUTRALITY - self.threshold)
                & rsi.shift(3).sgte(RSI_NEUTRALITY - self.threshold),
            rsi.slte(RSI_NEUTRALITY)
                & rsi.sgte(RSI_LOWER_BOUND)
                & rsi.shift(1).slte(RSI_NEUTRALITY + self.threshold)
                & rsi.shift(2).slte(RSI_NEUTRALITY + self.threshold)
                & rsi.shift(3).slte(RSI_NEUTRALITY + self.threshold),
        )
    }
}
