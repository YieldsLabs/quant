use base::prelude::*;
use core::prelude::*;
use trend::dpo;

const DPO_FILTER: f32 = 0.0;

pub struct DPOConfirm {
    smooth_type: Smooth,
    period: usize,
}

impl DPOConfirm {
    pub fn new(smooth_type: Smooth, period: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
        }
    }
}

impl Confirm for DPOConfirm {
    fn lookback(&self) -> usize {
        self.period
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let dpo = dpo(&data.close, self.smooth_type, self.period);

        (dpo.sgt(&DPO_FILTER), dpo.slt(&DPO_FILTER))
    }
}
