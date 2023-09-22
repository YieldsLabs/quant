use base::{OHLCVSeries, Signal};
use core::Series;
use shared::{ma_indicator, MovingAverageType};

pub struct Cross3MASignal {
    smoothing: MovingAverageType,
    short_period: usize,
    medium_period: usize,
    long_period: usize,
}

impl Cross3MASignal {
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

impl Signal for Cross3MASignal {
    fn id(&self) -> String {
        format!(
            "CROSS3MA_{}:{}:{}:{}",
            self.smoothing, self.short_period, self.medium_period, self.long_period
        )
    }

    fn lookback(&self) -> usize {
        let adjusted_lookback = std::cmp::max(self.short_period, self.long_period);
        std::cmp::max(adjusted_lookback, self.medium_period)
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let short_ma = ma_indicator(&self.smoothing, data, self.short_period);
        let medium_ma = ma_indicator(&self.smoothing, data, self.medium_period);
        let long_ma = ma_indicator(&self.smoothing, data, self.long_period);

        let long_signal = short_ma.cross_over(&medium_ma) & medium_ma.cross_over(&long_ma);
        let short_signal = short_ma.cross_under(&medium_ma) & medium_ma.cross_under(&long_ma);

        (long_signal, short_signal)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
