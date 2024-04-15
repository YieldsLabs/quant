use base::prelude::*;
use core::prelude::*;
use momentum::cci;

const CCI_UPPER_BARRIER: f32 = 50.;
const CCI_LOWER_BARRIER: f32 = -50.;

pub struct CciConfirm {
    smooth_type: Smooth,
    period: usize,
    factor: f32,
}

impl CciConfirm {
    pub fn new(smooth_type: Smooth, period: f32, factor: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
            factor,
        }
    }
}

impl Confirm for CciConfirm {
    fn lookback(&self) -> usize {
        self.period
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let cci = cci(&data.hlc3(), self.smooth_type, self.period, self.factor);

        (cci.sgt(&CCI_UPPER_BARRIER), cci.slt(&CCI_LOWER_BARRIER))
    }
}
