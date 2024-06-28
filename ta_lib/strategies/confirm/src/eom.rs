use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use volume::eom;

pub struct EomConfirm {
    source: SourceType,
    smooth: Smooth,
    period: usize,
}

impl EomConfirm {
    pub fn new(source: SourceType, smooth: Smooth, period: f32) -> Self {
        Self {
            source,
            smooth,
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
            &data.source(self.source),
            data.high(),
            data.low(),
            data.volume(),
            self.smooth,
            self.period,
        );

        (eom.sgt(&ZERO_LINE), eom.slt(&ZERO_LINE))
    }
}
