use base::prelude::*;
use core::prelude::*;
use shared::{ma_indicator, MovingAverageType};
use volatility::dch;

pub struct DCH2MASignal {
    dch_period: usize,
    ma: MovingAverageType,
    fast_period: usize,
    slow_period: usize,
}

impl DCH2MASignal {
    pub fn new(dch_period: f32, ma: MovingAverageType, fast_period: f32, slow_period: f32) -> Self {
        Self {
            dch_period: dch_period as usize,
            ma,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
        }
    }
}

impl Signal for DCH2MASignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.dch_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (upper_band, _, lower_band) = dch(&data.high, &data.low, self.dch_period);
        let ma_short = ma_indicator(&self.ma, data, self.fast_period);
        let ma_long = ma_indicator(&self.ma, data, self.slow_period);

        (
            data.close.sgt(&upper_band.shift(1)) & ma_short.sgt(&ma_long),
            data.close.slt(&lower_band.shift(1)) & ma_short.slt(&ma_long),
        )
    }
}
