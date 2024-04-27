use base::prelude::*;
use core::prelude::*;
use momentum::cfo;

pub struct CfoZeroCrossSignal {
    period: usize,
}

impl CfoZeroCrossSignal {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Signal for CfoZeroCrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let cfo = cfo(&data.close(), self.period);

        (cfo.cross_over(&ZERO_LINE), cfo.cross_under(&ZERO_LINE))
    }
}
