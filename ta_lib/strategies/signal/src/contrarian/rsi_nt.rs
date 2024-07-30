use base::prelude::*;
use core::prelude::*;
use momentum::rsi;
use timeseries::prelude::*;

const RSI_UPPER_BARRIER: f32 = 70.0;
const RSI_LOWER_BARRIER: f32 = 30.0;

pub struct RsiNtSignal {
    source: SourceType,
    smooth: Smooth,
    period: usize,
    threshold: f32,
}

impl RsiNtSignal {
    pub fn new(source: SourceType, smooth: Smooth, period: f32, threshold: f32) -> Self {
        Self {
            source,
            smooth,
            period: period as usize,
            threshold,
        }
    }
}

impl Signal for RsiNtSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.source(self.source), self.smooth, self.period);
        let low = data.low();
        let high = data.high();

        // let lower_barrier = RSI_LOWER_BARRIER + self.threshold;
        // let upper_barrier = RSI_UPPER_BARRIER - self.threshold;

        let prev_rsi = rsi.shift(1);

        (
            rsi.sgt(&prev_rsi)
                & rsi.slt(&RSI_LOWER_BARRIER)
                & prev_rsi.slt(&RSI_LOWER_BARRIER)
                & low.slt(&low.shift(1)),
            rsi.slt(&prev_rsi)
                & rsi.sgt(&RSI_UPPER_BARRIER)
                & prev_rsi.sgt(&RSI_UPPER_BARRIER)
                & high.sgt(&high.shift(1)),
        )
    }
}
