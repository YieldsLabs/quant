use base::prelude::*;
use core::prelude::*;
use momentum::tii;

pub struct TiiNeutralityCrossSignal {
    smooth_type: Smooth,
    major_period: usize,
    minor_period: usize,
}

impl TiiNeutralityCrossSignal {
    pub fn new(smooth_type: Smooth, major_period: f32, minor_period: f32) -> Self {
        Self {
            smooth_type,
            major_period: major_period as usize,
            minor_period: minor_period as usize,
        }
    }
}

impl Signal for TiiNeutralityCrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.minor_period, self.major_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tii = tii(
            &data.close(),
            self.smooth_type,
            self.major_period,
            self.minor_period,
        );

        (
            tii.cross_over(&NEUTRALITY_LINE),
            tii.cross_under(&NEUTRALITY_LINE),
        )
    }
}
