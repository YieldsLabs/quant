use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use volume::eom;

pub struct EomConfirm {
    source_type: SourceType,
    smooth_type: Smooth,
    period: usize,
}

impl EomConfirm {
    pub fn new(source_type: SourceType, smooth_type: Smooth, period: f32) -> Self {
        Self {
            source_type,
            smooth_type,
            period: period as usize,
        }
    }
}

impl Confirm for EomConfirm {
    fn lookback(&self) -> usize {
        self.period
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let eom = eom(
            &data.source(self.source_type),
            data.high(),
            data.low(),
            data.volume(),
            self.smooth_type,
            self.period,
        );

        (eom.sgt(&ZERO_LINE), eom.slt(&ZERO_LINE))
    }
}
