use base::prelude::*;
use core::prelude::*;
use trend::dpo;

const DPO_FILTER: f32 = 0.0;

pub struct DPOConfirm {
    period: usize,
}

impl DPOConfirm {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Confirm for DPOConfirm {
    fn lookback(&self) -> usize {
        self.period
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let dpo = dpo(&data.close, self.period);

        (dpo.sgt(&DPO_FILTER), dpo.slt(&DPO_FILTER))
    }
}
