use base::prelude::*;
use core::prelude::*;
use momentum::roc;
use timeseries::prelude::*;

pub struct RocZeroCrossSignal {
    source: SourceType,
    period: usize,
}

impl RocZeroCrossSignal {
    pub fn new(source: SourceType, period: f32) -> Self {
        Self {
            source,
            period: period as usize,
        }
    }
}

impl Signal for RocZeroCrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let roc = roc(&data.source(self.source), self.period);

        (roc.cross_over(&ZERO), roc.cross_under(&ZERO))
    }
}
