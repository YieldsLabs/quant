use base::prelude::*;
use core::prelude::*;
use momentum::trix;
use timeseries::prelude::*;

pub struct TrixExit {
    source_type: SourceType,
    smooth_type: Smooth,
    period: usize,
    signal_period: usize,
}

impl TrixExit {
    pub fn new(
        source_type: SourceType,
        smooth_type: Smooth,
        period: f32,
        signal_period: f32,
    ) -> Self {
        Self {
            source_type,
            smooth_type,
            period: period as usize,
            signal_period: signal_period as usize,
        }
    }
}

impl Exit for TrixExit {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.signal_period)
    }

    fn close(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let trix = trix(
            &data.source(self.source_type),
            self.smooth_type,
            self.period,
        );
        let signal_line = trix.smooth(self.smooth_type, self.signal_period);

        (
            trix.cross_under(&signal_line),
            trix.cross_over(&signal_line),
        )
    }
}
