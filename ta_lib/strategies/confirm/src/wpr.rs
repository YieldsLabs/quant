use base::prelude::*;
use core::prelude::*;
use momentum::wpr;
use timeseries::prelude::*;

pub struct WprConfirm {
    source: SourceType,
    period: usize,
    smooth_signal: Smooth,
    period_signal: usize,
}

impl WprConfirm {
    pub fn new(source: SourceType, period: f32, smooth_signal: Smooth, period_signal: f32) -> Self {
        Self {
            source,
            period: period as usize,
            smooth_signal,
            period_signal: period_signal as usize,
        }
    }
}

impl Confirm for WprConfirm {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.period_signal)
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let wrp = wpr(
            &data.source(self.source),
            data.high(),
            data.low(),
            self.period,
        );

        let signal = wrp.smooth(self.smooth_signal, self.period_signal);

        (wrp.sgt(&signal), wrp.slt(&signal))
    }
}
