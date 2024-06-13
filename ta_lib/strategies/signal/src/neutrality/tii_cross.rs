use base::prelude::*;
use core::prelude::*;
use momentum::tii;
use timeseries::prelude::*;

pub struct TiiNeutralityCrossSignal {
    source_type: SourceType,
    smooth_type: Smooth,
    major_period: usize,
    minor_period: usize,
}

impl TiiNeutralityCrossSignal {
    pub fn new(
        source_type: SourceType,
        smooth_type: Smooth,
        major_period: f32,
        minor_period: f32,
    ) -> Self {
        Self {
            source_type,
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

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tii = tii(
            &data.source(self.source_type),
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
