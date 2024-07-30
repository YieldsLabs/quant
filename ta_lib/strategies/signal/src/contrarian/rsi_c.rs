use base::prelude::*;
use core::prelude::*;
use momentum::rsi;
use osc::c;
use timeseries::prelude::*;

const RSI_UPPER_BARRIER: f32 = 70.0;
const RSI_LOWER_BARRIER: f32 = 30.0;

pub struct RsiCSignal {
    source: SourceType,
    smooth: Smooth,
    period: usize,
    threshold: f32,
}

impl RsiCSignal {
    pub fn new(source: SourceType, smooth: Smooth, period: f32, threshold: f32) -> Self {
        Self {
            source,
            smooth,
            period: period as usize,
            threshold,
        }
    }
}

impl Signal for RsiCSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        c!(
            rsi(&data.source(self.source), self.smooth, self.period),
            RSI_LOWER_BARRIER + self.threshold,
            RSI_UPPER_BARRIER - self.threshold
        )
    }
}
