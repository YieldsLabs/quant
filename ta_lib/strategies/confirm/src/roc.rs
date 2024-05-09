use base::prelude::*;
use core::prelude::*;
use momentum::roc;
use timeseries::prelude::*;

pub struct RocConfirm {
    source_type: SourceType,
    period: usize,
}

impl RocConfirm {
    pub fn new(source_type: SourceType, period: f32) -> Self {
        Self {
            source_type,
            period: period as usize,
        }
    }
}

impl Confirm for RocConfirm {
    fn lookback(&self) -> usize {
        self.period
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let roc = roc(&data.source(self.source_type), self.period);

        (roc.sgt(&ZERO_LINE), roc.slt(&ZERO_LINE))
    }
}
