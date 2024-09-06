use base::prelude::*;
use core::prelude::*;
use momentum::rex;
use timeseries::prelude::*;

pub struct RexExit {
    source: SourceType,
    smooth: Smooth,
    period: usize,
    smooth_signal: Smooth,
    period_signal: usize,
}

impl RexExit {
    pub fn new(
        source: SourceType,
        smooth: Smooth,
        period: f32,
        smooth_signal: Smooth,
        period_signal: f32,
    ) -> Self {
        Self {
            source,
            smooth,
            period: period as usize,
            smooth_signal,
            period_signal: period_signal as usize,
        }
    }
}

impl Exit for RexExit {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.period_signal)
    }

    fn close(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rex = rex(
            &data.source(self.source),
            data.open(),
            data.high(),
            data.low(),
            self.smooth,
            self.period,
        );

        let signal_line = rex.smooth(self.smooth_signal, self.period_signal);

        (rex.cross_under(&signal_line), rex.cross_over(&signal_line))
    }
}
