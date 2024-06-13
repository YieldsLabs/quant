use base::prelude::*;
use core::prelude::*;
use momentum::rsi;
use timeseries::prelude::*;

const RSI_UPPER_BARRIER: f32 = 80.0;
const RSI_LOWER_BARRIER: f32 = 20.0;

pub struct RsiVSignal {
    source_type: SourceType,
    smooth_type: Smooth,
    rsi_period: usize,
    threshold: f32,
}

impl RsiVSignal {
    pub fn new(
        source_type: SourceType,
        smooth_type: Smooth,
        rsi_period: f32,
        threshold: f32,
    ) -> Self {
        Self {
            source_type,
            smooth_type,
            rsi_period: rsi_period as usize,
            threshold,
        }
    }
}

impl Signal for RsiVSignal {
    fn lookback(&self) -> usize {
        self.rsi_period
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(
            &data.source(self.source_type),
            self.smooth_type,
            self.rsi_period,
        );
        let lower_barrier = RSI_LOWER_BARRIER + self.threshold;
        let upper_barrier = RSI_UPPER_BARRIER - self.threshold;

        let prev_rsi = rsi.shift(1);
        let rsi_2_back = rsi.shift(2);

        (
            rsi.sgt(&lower_barrier)
                & prev_rsi.slt(&RSI_LOWER_BARRIER)
                & rsi_2_back.sgt(&RSI_LOWER_BARRIER),
            rsi.slt(&upper_barrier)
                & prev_rsi.sgt(&RSI_UPPER_BARRIER)
                & rsi_2_back.slt(&RSI_UPPER_BARRIER),
        )
    }
}
