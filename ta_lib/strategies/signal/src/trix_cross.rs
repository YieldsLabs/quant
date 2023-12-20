use base::prelude::*;
use core::prelude::*;
use momentum::trix;

pub struct TRIXCrossSignal {
    period: usize,
    signal_period: usize,
}

impl TRIXCrossSignal {
    pub fn new(period: f32, signal_period: f32) -> Self {
        Self {
            period: period as usize,
            signal_period: signal_period as usize,
        }
    }
}

impl Signal for TRIXCrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.signal_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let trix = trix(&data.close, self.period);
        let signal_line = trix.ma(self.signal_period);

        (
            trix.cross_over(&signal_line),
            trix.cross_under(&signal_line),
        )
    }
}
