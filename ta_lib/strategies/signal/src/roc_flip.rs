use base::{OHLCVSeries, Signal};
use core::{Cross, Series};
use momentum::roc;

const ROC_ZERO: f32 = 0.0;

pub struct ROCFlipSignal {
    period: usize,
}

impl ROCFlipSignal {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Signal for ROCFlipSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let roc = roc(&data.close, self.period);

        (roc.cross_over(ROC_ZERO), roc.cross_under(ROC_ZERO))
    }
}
