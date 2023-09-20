use base::{BaseStrategy, OHLCVSeries, Signals};
use core::series::Series;
use filter::{map_to_filter, FilterConfig};
use momentum::rsi;
use shared::{ma, MovingAverageType};
use stop_loss::{map_to_stoploss, StopLossConfig};

pub struct RSI2xMAStrategy {
    rsi_period: usize,
    rsi_lower_barrier: usize,
    rsi_upper_barrier: usize,
    smoothing: MovingAverageType,
    short_period: usize,
    long_period: usize,
}

impl RSI2xMAStrategy {
    pub fn new(
        rsi_period: usize,
        rsi_lower_barrier: usize,
        rsi_upper_barrier: usize,
        smoothing: MovingAverageType,
        short_period: usize,
        long_period: usize,
        filter_config: FilterConfig,
        stoploss_config: StopLossConfig,
    ) -> BaseStrategy<RSI2xMAStrategy> {
        let signal = RSI2xMAStrategy {
            rsi_period,
            rsi_lower_barrier,
            rsi_upper_barrier,
            smoothing,
            short_period,
            long_period,
        };

        let filter = map_to_filter(filter_config);
        let stop_loss = map_to_stoploss(stoploss_config);

        let mut lookback_period = std::cmp::max(rsi_period, long_period);
        lookback_period = std::cmp::max(lookback_period, filter.lookback());

        BaseStrategy::new(signal, filter, stop_loss, lookback_period)
    }
}

impl Signals for RSI2xMAStrategy {
    fn id(&self) -> String {
        format!(
            "RSI2xMA_{}:{}:{}:{}:{}:{}",
            self.rsi_period,
            self.rsi_lower_barrier,
            self.rsi_upper_barrier,
            self.smoothing,
            self.short_period,
            self.long_period
        )
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma_short = ma(&self.smoothing, data, self.short_period);
        let ma_long = ma(&self.smoothing, data, self.long_period);
        let rsi = rsi(&data.close, self.rsi_period);
        let close = Series::from(&data.close);

        let long_signal = close.gt(&ma_short)
            & close.gt(&ma_long)
            & ma_short.gt(&ma_long)
            & rsi.slte(self.rsi_lower_barrier as f32)
            & rsi.shift(1).sgt(self.rsi_lower_barrier as f32);

        let short_signal = close.lt(&ma_short)
            & close.lt(&ma_long)
            & ma_short.lt(&ma_long)
            & rsi.sgte(self.rsi_upper_barrier as f32)
            & rsi.shift(1).slt(self.rsi_upper_barrier as f32);

        (long_signal, short_signal)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
