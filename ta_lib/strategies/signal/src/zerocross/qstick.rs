use base::prelude::*;
use core::prelude::*;
use momentum::qstick;
use timeseries::prelude::*;

pub struct QstickZeroCrossSignal {
    smooth_type: Smooth,
    period: usize,
}

impl QstickZeroCrossSignal {
    pub fn new(smooth_type: Smooth, period: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
        }
    }
}

impl Signal for QstickZeroCrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let qstick = qstick(data.open(), data.close(), self.smooth_type, self.period);

        (
            qstick.cross_over(&ZERO_LINE),
            qstick.cross_under(&ZERO_LINE),
        )
    }
}
