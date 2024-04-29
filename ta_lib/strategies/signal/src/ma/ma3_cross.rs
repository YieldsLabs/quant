use base::prelude::*;
use core::prelude::*;
use indicator::{ma_indicator, MovingAverageType};

pub struct Ma3CrossSignal {
    source_type: SourceType,
    ma: MovingAverageType,
    fast_period: usize,
    medium_period: usize,
    slow_period: usize,
}

impl Ma3CrossSignal {
    pub fn new(
        source_type: SourceType,
        ma: MovingAverageType,
        fast_period: f32,
        medium_period: f32,
        slow_period: f32,
    ) -> Self {
        Self {
            source_type,
            ma,
            fast_period: fast_period as usize,
            medium_period: medium_period as usize,
            slow_period: slow_period as usize,
        }
    }
}

impl Signal for Ma3CrossSignal {
    fn lookback(&self) -> usize {
        let adjusted_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adjusted_lookback, self.medium_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let short_ma = ma_indicator(&self.ma, data, self.source_type, self.fast_period);
        let medium_ma = ma_indicator(&self.ma, data, self.source_type, self.medium_period);
        let long_ma = ma_indicator(&self.ma, data, self.source_type, self.slow_period);

        (
            short_ma.cross_over(&medium_ma) & medium_ma.sgt(&long_ma),
            short_ma.cross_under(&medium_ma) & medium_ma.slt(&long_ma),
        )
    }
}
