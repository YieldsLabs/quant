use base::prelude::*;
use core::prelude::*;
use momentum::trix;
use timeseries::prelude::*;

pub struct TrixZeroCrossSignal {
    source: SourceType,
    smooth: Smooth,
    period: usize,
}

impl TrixZeroCrossSignal {
    pub fn new(source: SourceType, smooth: Smooth, period: f32) -> Self {
        Self {
            source,
            smooth,
            period: period as usize,
        }
    }
}

impl Signal for TrixZeroCrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let trix = trix(&data.source(self.source), self.smooth, self.period);

        (trix.cross_over(&ZERO), trix.cross_under(&ZERO))
    }
}
