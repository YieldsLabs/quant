use base::{OHLCVSeries, Signal};
use core::prelude::*;
use trend::qstick;

pub struct QSTICKCrossSignal {
    period: usize,
    signal_period: usize,
}

impl QSTICKCrossSignal {
    pub fn new(period: f32, signal_period: f32) -> Self {
        Self {
            period: period as usize,
            signal_period: signal_period as usize,
        }
    }
}

impl Signal for QSTICKCrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.signal_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let qstick = qstick(&data.open, &data.close, self.period);
        let signal_line = qstick.ema(self.signal_period);

        (
            qstick.cross_over(&signal_line),
            qstick.cross_under(&signal_line),
        )
    }
}
