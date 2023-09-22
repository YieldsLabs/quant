use base::{BaseStrategy, OHLCVSeries, Signals};
use core::Series;
use filter::{map_to_filter, FilterConfig};
use shared::{ma, MovingAverageType};
use stop_loss::{map_to_stoploss, StopLossConfig};

pub struct TestingGroundStrategy {
    long_period: usize,
    smoothing: MovingAverageType,
}

impl TestingGroundStrategy {
    pub fn new(
        smoothing: MovingAverageType,
        long_period: usize,
        filter_config: FilterConfig,
        stoploss_config: StopLossConfig,
    ) -> BaseStrategy<TestingGroundStrategy> {
        let signal = TestingGroundStrategy {
            long_period,
            smoothing,
        };
        let filter = map_to_filter(filter_config);
        let stop_loss = map_to_stoploss(stoploss_config);

        let lookback_period = std::cmp::max(long_period, filter.lookback());

        BaseStrategy::new(signal, filter, stop_loss, lookback_period)
    }
}

impl Signals for TestingGroundStrategy {
    fn id(&self) -> String {
        format!("GROUND_{}:{}", self.smoothing, self.long_period)
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma(&self.smoothing, data, self.long_period);

        let open = Series::from(&data.open);
        let high = Series::from(&data.high);
        let low = Series::from(&data.low);
        let close = Series::from(&data.close);

        let long_signal = low.lt(&ma)
            & low.shift(1).lt(&ma.shift(1))
            & low.shift(2).lt(&ma.shift(2))
            & close.min(&open).gt(&ma)
            & close.shift(1).min(&open.shift(1)).gt(&ma.shift(1))
            & close.shift(2).min(&open.shift(2)).gt(&ma.shift(2));

        let short_signal = high.gt(&ma)
            & high.shift(1).gt(&ma.shift(1))
            & high.shift(2).gt(&ma.shift(2))
            & close.max(&open).lt(&ma)
            & close.shift(1).max(&open.shift(1)).lt(&ma.shift(1))
            & close.shift(2).max(&open.shift(2)).lt(&ma.shift(2));

        (long_signal, short_signal)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
