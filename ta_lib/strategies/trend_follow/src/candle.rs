use base::{BaseStrategy, OHLCVSeries, Signals};
use core::series::Series;
use filter::{map_to_filter, FilterConfig};
use shared::{trend_candle, TrendCandleType};
use stop_loss::{map_to_stoploss, StopLossConfig};

pub struct CandleStrategy {
    candle: TrendCandleType,
}

impl CandleStrategy {
    pub fn new(
        candle: TrendCandleType,
        filter_config: FilterConfig,
        stoploss_config: StopLossConfig,
    ) -> BaseStrategy<CandleStrategy> {
        let signal = CandleStrategy { candle };

        let filter = map_to_filter(filter_config);
        let stop_loss = map_to_stoploss(stoploss_config);

        let lookback_period = filter.lookback();

        BaseStrategy::new(signal, filter, stop_loss, lookback_period)
    }
}

impl Signals for CandleStrategy {
    fn id(&self) -> String {
        format!("CANDLE_{}", self.candle)
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        trend_candle(&self.candle, data)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
