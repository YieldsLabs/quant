use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;

const DIDI_NEUTRALITY: f32 = 1.;

pub struct DidiConfirm {
    source: SourceType,
    smooth: Smooth,
    period_medium: usize,
    period_slow: usize,
    smooth_signal: Smooth,
    period_signal: usize,
}

impl DidiConfirm {
    pub fn new(
        source: SourceType,
        smooth: Smooth,
        period_medium: f32,
        period_slow: f32,
        smooth_signal: Smooth,
        period_signal: f32,
    ) -> Self {
        Self {
            source,
            smooth,
            period_medium: period_medium as usize,
            period_slow: period_slow as usize,
            smooth_signal,
            period_signal: period_signal as usize,
        }
    }
}

impl Confirm for DidiConfirm {
    fn lookback(&self) -> usize {
        std::cmp::max(
            self.period_signal,
            std::cmp::max(self.period_medium, self.period_slow),
        )
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let source = data.source(self.source);

        let med_line = source.smooth(self.smooth, self.period_medium);
        let long_line = source.smooth(self.smooth, self.period_slow) / med_line;

        let signal = long_line.smooth(self.smooth_signal, self.period_signal);

        (signal.sgt(&DIDI_NEUTRALITY), signal.slt(&DIDI_NEUTRALITY))
    }
}
