use base::{OHLCVSeries, Signal};
use core::Series;
use shared::{ma_indicator, rsi_indicator, MovingAverageType, RSIType};

pub struct RSI2MASignal {
    rsi_type: RSIType,
    rsi_period: usize,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: MovingAverageType,
    short_period: usize,
    long_period: usize,
}

impl RSI2MASignal {
    pub fn new(
        rsi_type: RSIType,
        rsi_period: f32,
        lower_barrier: f32,
        upper_barrier: f32,
        smoothing: MovingAverageType,
        short_period: f32,
        long_period: f32,
    ) -> Self {
        Self {
            rsi_type,
            rsi_period: rsi_period as usize,
            lower_barrier,
            upper_barrier,
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

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma_short = ma_indicator(&self.smoothing, data, self.short_period);
        let ma_long = ma_indicator(&self.smoothing, data, self.long_period);
        let rsi = rsi_indicator(&self.rsi_type, data, self.rsi_period);
        let close = Series::from(&data.close);

        let long_signal = close.gt(&ma_short)
            & close.gt(&ma_long)
            & ma_short.gt(&ma_long)
            & rsi.slte(self.lower_barrier)
            & rsi.shift(1).sgt(self.lower_barrier);

        let short_signal = close.lt(&ma_short)
            & close.lt(&ma_long)
            & ma_short.lt(&ma_long)
            & rsi.sgte(self.upper_barrier)
            & rsi.shift(1).slt(self.upper_barrier);

        (long_signal, short_signal)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
