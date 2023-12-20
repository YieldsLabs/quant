use base::{OHLCVSeries, Signal};
use core::prelude::*;
use trend::qstick;

const ZERO_LINE: f32 = 0.0;

pub struct QSTICKFlipSignal {
    period: usize,
}

impl QSTICKFlipSignal {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Signal for QSTICKFlipSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let qstick = qstick(&data.open, &data.close, self.period);

        (
            qstick.cross_over(&ZERO_LINE),
            qstick.cross_under(&ZERO_LINE),
        )
    }
}
