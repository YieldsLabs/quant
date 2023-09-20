use base::{BaseStrategy, OHLCVSeries, Signals};
use core::series::Series;
use filter::{map_to_filter, FilterConfig};
use momentum::rsi;
use shared::{ma, MovingAverageType};
use stop_loss::{map_to_stoploss, StopLossConfig};

pub struct RSIMAStrategy {
    rsi_period: usize,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: MovingAverageType,
    period: usize,
}

impl RSIMAStrategy {
    pub fn new(
        rsi_period: usize,
        lower_barrier: f32,
        upper_barrier: f32,
        smoothing: MovingAverageType,
        period: usize,
        filter_config: FilterConfig,
        stoploss_config: StopLossConfig,
    ) -> BaseStrategy<RSIMAStrategy> {
        let signal = RSIMAStrategy {
            rsi_period,
            lower_barrier,
            upper_barrier,
            smoothing,
            period,
        };

        let filter = map_to_filter(filter_config);
        let stop_loss = map_to_stoploss(stoploss_config);

        let mut lookback_period = std::cmp::max(rsi_period, period);
        lookback_period = std::cmp::max(lookback_period, filter.lookback());

        BaseStrategy::new(signal, filter, stop_loss, lookback_period)
    }
}

impl Signals for RSIMAStrategy {
    fn id(&self) -> String {
        format!(
            "RSIMA_{}:{}:{}:{}",
            self.lower_barrier, self.upper_barrier, self.smoothing, self.period
        )
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma(&self.smoothing, data, self.period);
        let rsi = rsi(&data.close, self.rsi_period);
        let close = Series::from(&data.close);

        let long_signal = ma.gt(&close) & rsi.slt(self.lower_barrier);
        let short_signal = ma.lt(&close) & rsi.sgt(self.upper_barrier);

        (long_signal, short_signal)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
