use base::prelude::*;
use core::prelude::*;
use momentum::cfo;
use timeseries::prelude::*;

pub struct CfoZeroCrossSignal {
    source_type: SourceType,
    period: usize,
}

impl CfoZeroCrossSignal {
    pub fn new(source_type: SourceType, period: f32) -> Self {
        Self {
            source_type,
            period: period as usize,
        }
    }
}

impl Signal for CfoZeroCrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let cfo = cfo(&data.source(self.source_type), self.period);

        (cfo.cross_over(&ZERO), cfo.cross_under(&ZERO))
    }
}
