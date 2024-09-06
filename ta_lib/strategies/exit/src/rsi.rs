use base::prelude::*;
use core::prelude::*;
use momentum::rsi;
use timeseries::prelude::*;

const RSI_OVERBOUGHT: f32 = 70.0;
const RSI_OVERSOLD: f32 = 30.0;

pub struct RsiExit {
    source_type: SourceType,
    smooth_type: Smooth,
    period: usize,
    threshold: f32,
}

impl RsiExit {
    pub fn new(source_type: SourceType, smooth_type: Smooth, period: f32, threshold: f32) -> Self {
        Self {
            source_type,
            smooth_type,
            period: period as usize,
            threshold,
        }
    }
}

impl Exit for RsiExit {
    fn lookback(&self) -> usize {
        self.period
    }

    fn close(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(
            &data.source(self.source_type),
            self.smooth_type,
            self.period,
        );

        let upper_bound = RSI_OVERBOUGHT - self.threshold;
        let lower_bound = RSI_OVERSOLD + self.threshold;

        (rsi.cross_under(&upper_bound), rsi.cross_over(&lower_bound))
    }
}
