use base::prelude::*;
use core::prelude::*;
use momentum::dso;
use timeseries::prelude::*;

pub struct DsoNeutralityCrossSignal {
    source_type: SourceType,
    smooth_type: Smooth,
    smooth_period: usize,
    k_period: usize,
    d_period: usize,
}

impl DsoNeutralityCrossSignal {
    pub fn new(
        source_type: SourceType,
        smooth_type: Smooth,
        smooth_period: f32,
        k_period: f32,
        d_period: f32,
    ) -> Self {
        Self {
            source_type,
            smooth_type,
            smooth_period: smooth_period as usize,
            k_period: k_period as usize,
            d_period: d_period as usize,
        }
    }
}

impl Signal for DsoNeutralityCrossSignal {
    fn lookback(&self) -> usize {
        let period = std::cmp::max(self.smooth_period, self.k_period);
        std::cmp::max(period, self.d_period)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (k, _) = dso(
            &data.source(self.source_type),
            self.smooth_type,
            self.smooth_period,
            self.k_period,
            self.d_period,
        );

        (k.cross_over(&NEUTRALITY), k.cross_under(&NEUTRALITY))
    }
}
