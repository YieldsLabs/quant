use base::prelude::*;
use core::prelude::*;
use momentum::di;

pub struct DICrossSignal {
    period: usize,
    signal_period: usize,
}

impl DICrossSignal {
    pub fn new(period: f32, signal_period: f32) -> Self {
        Self {
            period: period as usize,
            signal_period: signal_period as usize,
        }
    }
}

impl Signal for DICrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.signal_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let di = di(&data.close, self.period);
        let signal_line = di.smooth(Smooth::WMA, self.signal_period);

        (di.cross_over(&signal_line), di.cross_under(&signal_line))
    }
}
