use base::prelude::*;
use core::prelude::*;
use momentum::roc;
use timeseries::prelude::*;

pub struct RocZeroCrossSignal {
    source_type: SourceType,
    period: usize,
}

impl RocZeroCrossSignal {
    pub fn new(source_type: SourceType, period: f32) -> Self {
        Self {
            source_type,
            period: period as usize,
        }
    }
}

impl Signal for RocZeroCrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let roc = roc(&data.source(self.source_type), self.period);

        (roc.cross_over(&ZERO_LINE), roc.cross_under(&ZERO_LINE))
    }
}
