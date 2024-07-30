use base::prelude::*;
use core::prelude::*;
use momentum::rsi;
use timeseries::prelude::*;

pub struct RsiUSignal {
    source: SourceType,
    smooth: Smooth,
    period: usize,
    threshold: f32,
}

impl RsiUSignal {
    pub fn new(source: SourceType, smooth: Smooth, period: f32, threshold: f32) -> Self {
        Self {
            source,
            smooth,
            period: period as usize,
            threshold,
        }
    }
}

impl Signal for RsiUSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.source(self.source), self.smooth, self.period);
        let prev_rsi = rsi.shift(1);
        let back_2_rsi = rsi.shift(2);
        let back_3_rsi = rsi.shift(3);

        (
            rsi.sgt(&prev_rsi)
                & prev_rsi.seq(&back_2_rsi)
                & back_2_rsi.slt(&back_3_rsi)
                & rsi.slt(&NEUTRALITY_LINE),
            rsi.slt(&prev_rsi)
                & prev_rsi.seq(&back_2_rsi)
                & back_2_rsi.sgt(&back_3_rsi)
                & rsi.sgt(&NEUTRALITY_LINE),
        )
    }
}
