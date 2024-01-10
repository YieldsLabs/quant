use base::prelude::*;
use core::prelude::*;
use momentum::tii;

const TII_UPPER_BARRIER: f32 = 80.0;
const TII_LOWER_BARRIER: f32 = 20.0;

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
            tii.sgt(&TII_LOWER_BARRIER)
                & tii.shift(1).slt(&TII_LOWER_BARRIER)
                & tii.shift(2).sgt(&TII_LOWER_BARRIER),
            tii.slt(&TII_UPPER_BARRIER)
                & tii.shift(1).sgt(&TII_UPPER_BARRIER)
                & tii.shift(2).slt(&TII_UPPER_BARRIER),
        )
    }
}
