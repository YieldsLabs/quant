use base::prelude::*;
use core::prelude::*;
use momentum::tii;
use timeseries::prelude::*;

const TII_UPPER_BARRIER: f32 = 100.0;
const TII_LOWER_BARRIER: f32 = 0.0;

pub struct TiiVSignal {
    source: SourceType,
    smooth: Smooth,
    major_period: usize,
    minor_period: usize,
}

impl TiiVSignal {
    pub fn new(source: SourceType, smooth: Smooth, major_period: f32, minor_period: f32) -> Self {
        Self {
            source,
            smooth,
            major_period: major_period as usize,
            minor_period: minor_period as usize,
        }
    }
}

impl Signal for TiiVSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.minor_period, self.major_period)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tii = tii(
            &data.source(self.source),
            self.smooth,
            self.major_period,
            self.minor_period,
        );

        let prev_tii = tii.shift(1);
        let tii_2_back = tii.shift(2);

        (
            tii.sgt(&TII_LOWER_BARRIER)
                & prev_tii.seq(&TII_LOWER_BARRIER)
                & tii_2_back.sgt(&TII_LOWER_BARRIER),
            tii.slt(&TII_UPPER_BARRIER)
                & prev_tii.seq(&TII_UPPER_BARRIER)
                & tii_2_back.slt(&TII_UPPER_BARRIER),
        )
    }
}
