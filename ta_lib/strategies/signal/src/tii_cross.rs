use base::{OHLCVSeries, Signal};
use core::Series;
use trend::tii;

pub struct TIICrossSignal {
    major_period: usize,
    minor_period: usize,
    lower_barrier: f32,
    upper_barrier: f32,
}

impl TIICrossSignal {
    pub fn new(
        major_period: f32,
        minor_period: f32,
        lower_barrier: f32,
        upper_barrier: f32,
    ) -> Self {
        Self {
            major_period: major_period as usize,
            minor_period: minor_period as usize,
            lower_barrier,
            upper_barrier,
        }
    }
}

impl Signal for TIICrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.minor_period, self.major_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tii = tii(&data.close, self.major_period, self.minor_period);

        let long_signal = tii.cross_over_line(self.upper_barrier);
        let short_signal = tii.cross_under_line(self.lower_barrier);

        (long_signal, short_signal)
    }
}
