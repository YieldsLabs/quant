use base::{Filter, OHLCVSeries};
use core::series::Series;
use momentum::rsi;

pub struct RSIFilter {
    period: usize,
    threshold: f32,
}

impl RSIFilter {
    pub fn new(period: usize, threshold: f32) -> Self {
        Self { period, threshold }
    }
}

impl Filter for RSIFilter {
    fn id(&self) -> String {
        format!("FRSI_{}_{:.1}", self.period, self.threshold)
    }

    fn lookback(&self) -> usize {
        self.period
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.close, self.period);

        (rsi.sgt(self.threshold), rsi.slt(self.threshold))
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
