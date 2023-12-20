use base::{Filter, OHLCVSeries};
use core::prelude::*;
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
        let lower_neutrality = RSI_NEUTRALITY - self.threshold;
        let upper_neutrality = RSI_NEUTRALITY + self.threshold;

        (
            rsi.sge(&RSI_NEUTRALITY)
                & rsi.sle(&RSI_UPPER_BOUND)
                & rsi.shift(1).sge(&lower_neutrality)
                & rsi.shift(2).sge(&lower_neutrality)
                & rsi.shift(3).sge(&lower_neutrality),
            rsi.sle(&RSI_NEUTRALITY)
                & rsi.sge(&RSI_LOWER_BOUND)
                & rsi.shift(1).sle(&upper_neutrality)
                & rsi.shift(2).sle(&upper_neutrality)
                & rsi.shift(3).sle(&upper_neutrality),
        )
    }
}
