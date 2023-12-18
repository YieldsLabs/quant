use base::{OHLCVSeries, Signal};
use core::{Cross, Series};
use shared::{ma_indicator, rsi_indicator, MovingAverageType, RSIType};

const RSI_UPPER_BARRIER: f32 = 85.0;
const RSI_LOWER_BARRIER: f32 = 15.0;

pub struct RSI2MASignal {
    rsi_type: RSIType,
    rsi_period: usize,
    threshold: f32,
    smoothing: MovingAverageType,
    short_period: usize,
    long_period: usize,
}

impl RSI2MASignal {
    pub fn new(
        rsi_type: RSIType,
        rsi_period: f32,
        threshold: f32,
        smoothing: MovingAverageType,
        short_period: f32,
        long_period: f32,
    ) -> Self {
        Self {
            rsi_type,
            rsi_period: rsi_period as usize,
            threshold,
            smoothing,
            short_period: short_period as usize,
            long_period: long_period as usize,
        }
    }
}

impl Signal for RSI2MASignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.short_period, self.long_period);
        std::cmp::max(adj_lookback, self.rsi_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi_indicator(&self.rsi_type, data, self.rsi_period);
        let ma_short = ma_indicator(&self.smoothing, data, self.short_period);
        let ma_long = ma_indicator(&self.smoothing, data, self.long_period);

        let long_signal = data.close.gt(&ma_short)
            & data.close.gt(&ma_long)
            & ma_short.gt(&ma_long)
            & rsi.cross_under(RSI_LOWER_BARRIER + self.threshold);

        let short_signal = data.close.lt(&ma_short)
            & data.close.lt(&ma_long)
            & ma_short.lt(&ma_long)
            & rsi.cross_over(RSI_UPPER_BARRIER - self.threshold);

        (long_signal, short_signal)
    }
}
