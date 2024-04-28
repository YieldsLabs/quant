use base::prelude::*;
use core::prelude::*;
use trend::dpo;

pub struct DpoConfirm {
    smooth_type: Smooth,
    period: usize,
}

impl DpoConfirm {
    pub fn new(smooth_type: Smooth, period: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
        }
    }
}

impl Confirm for DpoConfirm {
    fn lookback(&self) -> usize {
        self.period
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let dpo = dpo(data.close(), self.smooth_type, self.period);

        (dpo.sgt(&ZERO_LINE), dpo.slt(&ZERO_LINE))
    }
}
