use base::prelude::*;
use core::prelude::*;
use shared::{ma_indicator, MovingAverageType};

pub struct MA3CrossSignal {
    smoothing: MovingAverageType,
    short_period: usize,
    medium_period: usize,
    long_period: usize,
}

impl MA3CrossSignal {
    pub fn new(
        smoothing: MovingAverageType,
        short_period: f32,
        medium_period: f32,
        long_period: f32,
    ) -> Self {
        Self {
            smoothing,
            short_period: short_period as usize,
            medium_period: medium_period as usize,
            long_period: long_period as usize,
        }
    }
}

impl Signal for MA3CrossSignal {
    fn lookback(&self) -> usize {
        let adjusted_lookback = std::cmp::max(self.short_period, self.long_period);
        std::cmp::max(adjusted_lookback, self.medium_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let short_ma = ma_indicator(&self.smoothing, data, self.short_period);
        let medium_ma = ma_indicator(&self.smoothing, data, self.medium_period);
        let long_ma = ma_indicator(&self.smoothing, data, self.long_period);

        (
            short_ma.cross_over(&medium_ma) & medium_ma.sgt(&long_ma),
            short_ma.cross_under(&medium_ma) & medium_ma.slt(&long_ma),
        )
    }
}
