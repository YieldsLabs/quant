use base::{Filter, OHLCVSeries, Price};
use core::Series;
use trend::dmi;

pub struct ADXFilter {
    smoothing_period: usize,
    di_period: usize,
    atr_period: usize,
    threshold: f32,
}

impl ADXFilter {
    pub fn new(smoothing_period: f32, di_period: f32, atr_period: f32, threshold: f32) -> Self {
        Self {
            smoothing_period: smoothing_period as usize,
            di_period: di_period as usize,
            atr_period: atr_period as usize,
            threshold,
        }
    }
}

impl Filter for ADXFilter {
    fn lookback(&self) -> usize {
        let adjusted_lookback = std::cmp::max(self.smoothing_period, self.di_period);
        std::cmp::max(adjusted_lookback, self.atr_period)
    }

    fn apply(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (adx, _, _) = dmi(
            &data.high,
            &data.low,
            &data.atr(self.atr_period),
            self.smoothing_period,
            self.di_period,
        );

        (adx.sgt(self.threshold), adx.sgt(self.threshold))
    }
}
