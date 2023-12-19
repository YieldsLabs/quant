use base::{OHLCVSeries, Signal};
use core::{Comparator, Series};
use shared::{ma_indicator, MovingAverageType};
use volatility::dch;

pub struct DCH2MASignal {
    dch_period: usize,
    smoothing: MovingAverageType,
    short_period: usize,
    long_period: usize,
}

impl DCH2MASignal {
    pub fn new(
        dch_period: f32,
        smoothing: MovingAverageType,
        short_period: f32,
        long_period: f32,
    ) -> Self {
        Self {
            dch_period: dch_period as usize,
            smoothing,
            short_period: short_period as usize,
            long_period: long_period as usize,
        }
    }
}

impl Signal for DCH2MASignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.short_period, self.long_period);
        std::cmp::max(adj_lookback, self.dch_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (upper_band, _, lower_band) = dch(&data.high, &data.low, self.dch_period);
        let ma_short = ma_indicator(&self.smoothing, data, self.short_period);
        let ma_long = ma_indicator(&self.smoothing, data, self.long_period);

        (
            data.close.sgt(&upper_band.shift(1)) & ma_short.sgt(&ma_long),
            data.close.slt(&lower_band.shift(1)) & ma_short.slt(&ma_long),
        )
    }
}
