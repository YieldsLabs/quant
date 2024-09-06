use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use trail::f;
use trend::ce;

pub struct CeFlipSignal {
    source_type: SourceType,
    period: usize,
    smooth_atr: Smooth,
    period_atr: usize,
    factor: f32,
}

impl CeFlipSignal {
    pub fn new(
        source_type: SourceType,
        period: f32,
        smooth_atr: Smooth,
        period_atr: f32,
        factor: f32,
    ) -> Self {
        Self {
            source_type,
            period: period as usize,
            smooth_atr,
            period_atr: period_atr as usize,
            factor,
        }
    }
}

impl Signal for CeFlipSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.period_atr)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (direction, _) = ce(
            &data.source(self.source_type),
            &data.atr(self.smooth_atr, self.period_atr),
            self.period,
            self.factor,
        );

        f!(direction)
    }
}
