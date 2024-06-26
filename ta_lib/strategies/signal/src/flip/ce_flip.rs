use base::prelude::*;
use core::prelude::*;
use trend::ce;

pub struct CeFlipSignal {
    period: usize,
    atr_period: usize,
    factor: f32,
}

impl CeFlipSignal {
    pub fn new(period: f32, atr_period: f32, factor: f32) -> Self {
        Self {
            period: period as usize,
            atr_period: atr_period as usize,
            factor,
        }
    }
}

impl Signal for CeFlipSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.atr_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (direction, _) = ce(
            data.close(),
            &data.atr(self.atr_period),
            self.period,
            self.factor,
        );

        (direction.cross_under(&ZERO), direction.cross_over(&ZERO))
    }
}
