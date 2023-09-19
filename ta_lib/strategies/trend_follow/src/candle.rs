use base::{BaseStrategy, OHLCVSeries, Signals};
use core::series::Series;
use filter::{map_to_filter, FilterConfig};
use shared::{trend_candle, TrendCandleType};
use stop_loss::ATRStopLoss;

pub struct CandleStrategy {
    candle: TrendCandleType,
}

impl CandleStrategy {
    pub fn new(
        candle: TrendCandleType,
        filter_config: FilterConfig,
        atr_period: usize,
        stop_loss_multi: f32,
    ) -> BaseStrategy<CandleStrategy, ATRStopLoss> {
        let signal = CandleStrategy { candle };

        let filter = map_to_filter(filter_config);

        let lookback_period = filter.lookback();

        let stop_loss = ATRStopLoss {
            atr_period,
            multi: stop_loss_multi,
        };

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
