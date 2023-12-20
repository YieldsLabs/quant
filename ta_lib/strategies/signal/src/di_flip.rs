use base::prelude::*;
use core::prelude::*;
use momentum::di;

const ZERO_LINE: f32 = 0.0;

pub struct DIFlipSignal {
    period: usize,
}

impl DIFlipSignal {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Signal for DIFlipSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let di = di(&data.close, self.period, None);

        (di.cross_over(&ZERO_LINE), di.cross_under(&ZERO_LINE))
    }
}
