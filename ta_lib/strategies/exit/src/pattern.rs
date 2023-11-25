use base::{Exit, OHLCVSeries};
use candlestick::{doji, engulfing};
use core::Series;

pub struct PatternExit {
    period: usize,
}

impl PatternExit {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Exit for PatternExit {
    fn lookback(&self) -> usize {
        self.period
    }

    fn evaluate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (
            doji::bearish(&data.open, &data.close),
            engulfing::bullish(&data.open, &data.high, &data.low, &data.close),
        )
    }
}
