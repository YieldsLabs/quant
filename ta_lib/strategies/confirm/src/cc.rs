use base::prelude::*;
use core::prelude::*;
use momentum::cc;
use timeseries::prelude::*;

pub struct CcConfirm {
    source: SourceType,
    period_fast: usize,
    period_slow: usize,
    smooth: Smooth,
    period_smooth: usize,
    smooth_signal: Smooth,
    period_signal: usize,
}

impl CcConfirm {
    pub fn new(
        source: SourceType,
        period_fast: f32,
        period_slow: f32,
        smooth: Smooth,
        period_smooth: f32,
        smooth_signal: Smooth,
        period_signal: f32,
    ) -> Self {
        Self {
            source,
            period_fast: period_fast as usize,
            period_slow: period_slow as usize,
            smooth,
            period_smooth: period_smooth as usize,
            smooth_signal,
            period_signal: period_signal as usize,
        }
    }
}

impl Confirm for CcConfirm {
    fn lookback(&self) -> usize {
        std::cmp::max(
            std::cmp::max(self.period_fast, self.period_slow),
            std::cmp::max(self.period_smooth, self.period_signal),
        )
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let cc = cc(
            &data.source(self.source),
            self.period_fast,
            self.period_slow,
            self.smooth,
            self.period_smooth,
        );
        let prev_cc = cc.shift(1);

        let signal = cc.smooth(self.smooth_signal, self.period_signal);

        (
            cc.sgt(&signal) & cc.sgt(&prev_cc),
            cc.slt(&signal) & cc.slt(&prev_cc),
        )
    }
}
