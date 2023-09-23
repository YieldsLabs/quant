use base::{Filter, OHLCVSeries};
use core::Series;
use shared::{rsi_indicator, RSIType};

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

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi_indicator(&self.rsi_type, data, self.period);

        (rsi.slte(self.threshold), rsi.sgte(self.threshold))
    }
}
