use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use trend::qstick;

pub struct QstickSignalLineSignal {
    smooth_type: Smooth,
    period: usize,
    signal_period: usize,
}

impl QstickSignalLineSignal {
    pub fn new(smooth_type: Smooth, period: f32, signal_period: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
            signal_period: signal_period as usize,
        }
    }
}

impl Signal for QstickSignalLineSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.signal_period)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let qstick = qstick(data.open(), data.close(), self.smooth_type, self.period);
        let signal_line = qstick.smooth(self.smooth_type, self.signal_period);

        (
            qstick.cross_over(&signal_line),
            qstick.cross_under(&signal_line),
        )
    }
}
