use base::{OHLCVSeries, Signal};
use core::Series;
use shared::{ma_indicator, MovingAverageType};

pub struct Cross2MASignal {
    smoothing: MovingAverageType,
    short_period: usize,
    long_period: usize,
}

impl Cross2MASignal {
    pub fn new(smoothing: MovingAverageType, short_period: f32, long_period: f32) -> Self {
        Self {
            smoothing,
            short_period: short_period as usize,
            long_period: long_period as usize,
        }
    }
}

impl Signal for Cross2MASignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.short_period, self.long_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let short_ma = ma_indicator(&self.smoothing, data, self.short_period);
        let long_ma = ma_indicator(&self.smoothing, data, self.long_period);

        let long_signal = short_ma.cross_over(&long_ma);
        let short_signal = short_ma.cross_under(&long_ma);

        (long_signal, short_signal)
    }
}
