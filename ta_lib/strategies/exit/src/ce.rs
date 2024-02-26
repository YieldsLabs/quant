use base::prelude::*;
use core::prelude::*;
use trend::ce;

pub struct CeExit {
    period: usize,
    atr_period: usize,
    factor: f32,
}

impl CeExit {
    pub fn new(period: f32, atr_period: f32, factor: f32) -> Self {
        Self {
            period: period as usize,
            atr_period: atr_period as usize,
            factor,
        }
    }
}

impl Exit for CeExit {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.atr_period)
    }

    fn evaluate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (direction, _) = ce(
            &data.high,
            &data.low,
            &data.close,
            &data.atr(self.atr_period, Smooth::SMMA),
            self.period,
            self.factor,
        );

        let prev_direction = direction.shift(1);

        (
            direction.seq(&-1.0) & prev_direction.seq(&1.0),
            direction.seq(&1.0) & prev_direction.seq(&-1.0),
        )
    }
}
