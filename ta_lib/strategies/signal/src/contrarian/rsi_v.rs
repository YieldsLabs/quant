use base::prelude::*;
use core::prelude::*;
use momentum::rsi;
use osc::v;
use timeseries::prelude::*;

const RSI_UPPER_BARRIER: f32 = 80.0;
const RSI_LOWER_BARRIER: f32 = 20.0;

pub struct RsiVSignal {
    source: SourceType,
    smooth: Smooth,
    period: usize,
    threshold: f32,
}

impl RsiVSignal {
    pub fn new(source: SourceType, smooth: Smooth, period: f32, threshold: f32) -> Self {
        Self {
            source,
            smooth,
            period: period as usize,
            threshold,
        }
    }
}

impl Signal for RsiVSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.source(self.source), self.smooth, self.period);

        let lower_barrier = RSI_LOWER_BARRIER + self.threshold;
        let upper_barrier = RSI_UPPER_BARRIER - self.threshold;

        v!(rsi, lower_barrier, upper_barrier)
    }
}
