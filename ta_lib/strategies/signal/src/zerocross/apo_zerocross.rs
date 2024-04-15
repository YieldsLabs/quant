use base::prelude::*;
use core::prelude::*;
use momentum::apo;

pub struct ApoZeroCrossSignal {
    fast_period: usize,
    slow_period: usize,
}

impl ApoZeroCrossSignal {
    pub fn new(fast_period: f32, slow_period: f32) -> Self {
        Self {
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
        }
    }
}

impl Signal for ApoZeroCrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.fast_period, self.slow_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let apo = apo(&data.close, self.fast_period, self.slow_period);

        (apo.cross_over(&ZERO_LINE), apo.cross_under(&ZERO_LINE))
    }
}
