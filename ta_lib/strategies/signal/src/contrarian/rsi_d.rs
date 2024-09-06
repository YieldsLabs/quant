use base::prelude::*;
use core::prelude::*;
use momentum::rsi;
use timeseries::prelude::*;

const RSI_UPPER_BARRIER: f32 = 80.0;
const RSI_LOWER_BARRIER: f32 = 20.0;

pub struct RsiDSignal {
    source: SourceType,
    smooth: Smooth,
    period: usize,
    threshold: f32,
}

impl RsiDSignal {
    pub fn new(source: SourceType, smooth: Smooth, period: f32, threshold: f32) -> Self {
        Self {
            source,
            smooth,
            period: period as usize,
            threshold,
        }
    }
}

impl Signal for RsiDSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.source(self.source), self.smooth, self.period);
        let lower_barrier = RSI_LOWER_BARRIER + self.threshold;
        let upper_barrier = RSI_UPPER_BARRIER - self.threshold;

        let prev_rsi = rsi.shift(1);
        let back_2_rsi = rsi.shift(2);
        let back_3_rsi = rsi.shift(3);
        let back_4_rsi = rsi.shift(4);

        (
            rsi.slt(&prev_rsi)
                & prev_rsi.slt(&back_2_rsi)
                & back_2_rsi.slt(&back_3_rsi)
                & back_3_rsi.slt(&lower_barrier)
                & back_4_rsi.sgt(&lower_barrier),
            rsi.sgt(&prev_rsi)
                & prev_rsi.sgt(&back_2_rsi)
                & back_2_rsi.sgt(&back_3_rsi)
                & back_3_rsi.sgt(&upper_barrier)
                & back_4_rsi.slt(&upper_barrier),
        )
    }
}
