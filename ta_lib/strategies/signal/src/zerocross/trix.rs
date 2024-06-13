use base::prelude::*;
use core::prelude::*;
use momentum::trix;
use timeseries::prelude::*;

pub struct TrixZeroCrossSignal {
    source_type: SourceType,
    smooth_type: Smooth,
    period: usize,
}

impl TrixZeroCrossSignal {
    pub fn new(source_type: SourceType, smooth_type: Smooth, period: f32) -> Self {
        Self {
            source_type,
            smooth_type,
            period: period as usize,
        }
    }
}

impl Signal for TrixZeroCrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let trix = trix(
            &data.source(self.source_type),
            self.smooth_type,
            self.period,
        );

        (trix.cross_over(&ZERO_LINE), trix.cross_under(&ZERO_LINE))
    }
}
