use base::prelude::*;
use core::prelude::*;
use momentum::di;

pub struct DiSignalLineSignal {
    smooth_type: Smooth,
    period: usize,
    signal_period: usize,
}

impl DiSignalLineSignal {
    pub fn new(smooth_type: Smooth, period: f32, signal_period: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
            signal_period: signal_period as usize,
        }
    }
}

impl Signal for DiSignalLineSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.signal_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let di = di(&data.close(), self.smooth_type, self.period);
        let signal_line = di.smooth(self.smooth_type, self.signal_period);

        (di.cross_over(&signal_line), di.cross_under(&signal_line))
    }
}
