use base::{OHLCVSeries, Signal};
use core::{Comparator, Cross, Series};
use momentum::tii;

const TII_UPPER_BARRIER: f32 = 60.0;
const TII_LOWER_BARRIER: f32 = 40.0;

pub struct TIICrossSignal {
    major_period: usize,
    minor_period: usize,
    threshold: f32,
}

impl TIICrossSignal {
    pub fn new(major_period: f32, minor_period: f32, threshold: f32) -> Self {
        Self {
            major_period: major_period as usize,
            minor_period: minor_period as usize,
            threshold,
        }
    }
}

impl Signal for TIICrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.minor_period, self.major_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tii = tii(&data.close, self.major_period, self.minor_period);

        (
            tii.cross_over(&(TII_UPPER_BARRIER + self.threshold)),
            tii.cross_under(&(TII_LOWER_BARRIER - self.threshold)),
        )
    }
}
