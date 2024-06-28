use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use trend::dpo;

const DPO_UPPER_BARRIER: f32 = 0.005;
const DPO_LOWER_BARRIER: f32 = -0.005;

pub struct DpoConfirm {
    source: SourceType,
    smooth: Smooth,
    period: usize,
}

impl DpoConfirm {
    pub fn new(source: SourceType, smooth: Smooth, period: f32) -> Self {
        Self {
            source,
            smooth,
            period: period as usize,
        }
    }
}

impl Confirm for DpoConfirm {
    fn lookback(&self) -> usize {
        self.period
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let dpo = dpo(&data.source(self.source), self.smooth, self.period);

        (dpo.sgt(&DPO_UPPER_BARRIER), dpo.slt(&DPO_LOWER_BARRIER))
    }
}
