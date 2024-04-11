use base::prelude::*;
use core::prelude::*;
use momentum::roc;

pub struct ROCConfirm {
    period: usize,
}

impl ROCConfirm {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Confirm for ROCConfirm {
    fn lookback(&self) -> usize {
        self.period
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let roc = roc(&data.close, self.period);

        (roc.sgt(&ZERO_LINE), roc.slt(&ZERO_LINE))
    }
}
