use base::prelude::*;
use core::prelude::*;
use momentum::tdfi;

const TDFI_UPPER_LINE: f32 = 0.05;
const TDFI_LOWER_LINE: f32 = -0.05;

pub struct TDFIPulse {
    smooth_type: Smooth,
    period: usize,
    n: usize,
}

impl TDFIPulse {
    pub fn new(smooth_type: Smooth, period: f32, n: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
            n: n as usize,
        }
    }
}

impl Pulse for TDFIPulse {
    fn lookback(&self) -> usize {
        self.period
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tdfi = tdfi(&data.close, self.smooth_type, self.period, self.n);

        (tdfi.sgt(&TDFI_UPPER_LINE), tdfi.slt(&TDFI_LOWER_LINE))
    }
}
