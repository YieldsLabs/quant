use base::{Regime, OHLCVSeries};
use core::Series;
use shared::{rsi_indicator, RSIType};

const RSI_NEUTRALITY: f32 = 50.0;

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

impl Regime for RSIFilter {
    fn lookback(&self) -> usize {
        self.period
    }

    fn apply(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi_indicator(&self.rsi_type, data, self.period);

        (
            rsi.sgt(RSI_NEUTRALITY + self.threshold),
            rsi.slt(RSI_NEUTRALITY - self.threshold),
        )
    }
}
