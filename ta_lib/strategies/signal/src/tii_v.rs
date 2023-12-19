use base::{OHLCVSeries, Signal};
use core::{Comparator, Series};
use momentum::tii;

const TII_ZERO: f32 = 0.0;
const TII_ONEH: f32 = 100.0;

pub struct TIIVSignal {
    major_period: usize,
    minor_period: usize,
}

impl TIIVSignal {
    pub fn new(major_period: f32, minor_period: f32) -> Self {
        Self {
            major_period: major_period as usize,
            minor_period: minor_period as usize,
        }
    }
}

impl Signal for TIIVSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.minor_period, self.major_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tii = tii(&data.close, self.major_period, self.minor_period);

        (
            tii.sgt(&TII_ZERO) & tii.shift(1).seq(&TII_ZERO) & tii.shift(2).sgt(&TII_ZERO),
            tii.slt(&TII_ONEH) & tii.shift(1).seq(&TII_ONEH) & tii.shift(2).slt(&TII_ONEH),
        )
    }
}
