use base::prelude::*;
use core::prelude::*;
use momentum::rsi;
use shared::{ma_indicator, MovingAverageType};

const RSI_UPPER_BARRIER: f32 = 85.0;
const RSI_LOWER_BARRIER: f32 = 15.0;

pub struct RSI2MASignal {
    smooth_type: Smooth,
    rsi_period: usize,
    threshold: f32,
    ma: MovingAverageType,
    fast_period: usize,
    slow_period: usize,
}

impl RSI2MASignal {
    pub fn new(
        smooth_type: Smooth,
        rsi_period: f32,
        threshold: f32,
        ma: MovingAverageType,
        fast_period: f32,
        slow_period: f32,
    ) -> Self {
        Self {
            smooth_type,
            rsi_period: rsi_period as usize,
            threshold,
            ma,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
        }
    }
}

impl Signal for RSI2MASignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.rsi_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.close, self.smooth_type, self.rsi_period);
        let ma_short = ma_indicator(&self.ma, data, self.fast_period);
        let ma_long = ma_indicator(&self.ma, data, self.slow_period);
        let lower_barrier = RSI_LOWER_BARRIER + self.threshold;
        let upper_barrier = RSI_UPPER_BARRIER - self.threshold;

        (
            data.close.sgt(&ma_short)
                & data.close.sgt(&ma_long)
                & ma_short.sgt(&ma_long)
                & rsi.cross_under(&lower_barrier),
            data.close.slt(&ma_short)
                & data.close.slt(&ma_long)
                & ma_short.slt(&ma_long)
                & rsi.cross_over(&upper_barrier),
        )
    }
}
