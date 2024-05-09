use base::prelude::*;
use core::prelude::*;
use momentum::ao;
use timeseries::prelude::*;

pub struct AoSaucerSignal {
    source_type: SourceType,
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
}

impl AoSaucerSignal {
    pub fn new(
        source_type: SourceType,
        smooth_type: Smooth,
        fast_period: f32,
        slow_period: f32,
    ) -> Self {
        Self {
            source_type,
            smooth_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
        }
    }
}

impl Signal for AoSaucerSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.fast_period, self.slow_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ao = ao(
            &data.source(self.source_type),
            self.smooth_type,
            self.fast_period,
            self.slow_period,
        );
        let diff = &ao - ao.shift(1);

        let prev_diff = diff.shift(1);
        let back_2_diff = diff.shift(2);

        (
            ao.sgt(&ZERO_LINE)
                & diff.sgt(&ZERO_LINE)
                & diff.sgt(&prev_diff)
                & prev_diff.slt(&ZERO_LINE)
                & back_2_diff.slt(&ZERO_LINE)
                & prev_diff.slt(&back_2_diff),
            ao.slt(&ZERO_LINE)
                & diff.slt(&ZERO_LINE)
                & diff.slt(&prev_diff)
                & prev_diff.sgt(&ZERO_LINE)
                & back_2_diff.sgt(&ZERO_LINE)
                & prev_diff.slt(&back_2_diff),
        )
    }
}
