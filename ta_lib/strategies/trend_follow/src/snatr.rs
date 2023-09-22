use base::{BaseStrategy, OHLCVSeries, Signals};
use core::Series;
use filter::{map_to_filter, FilterConfig};
use stop_loss::{map_to_stoploss, StopLossConfig};
use volatility::snatr;

pub struct SNATRStrategy {
    atr_period: usize,
    atr_smoothing_period: usize,
}

impl SNATRStrategy {
    pub fn new(
        atr_period: usize,
        atr_smoothing_period: usize,
        filter_config: FilterConfig,
        stoploss_config: StopLossConfig,
    ) -> BaseStrategy<SNATRStrategy> {
        let signal = SNATRStrategy {
            atr_period,
            atr_smoothing_period,
        };

        let filter = map_to_filter(filter_config);
        let stop_loss = map_to_stoploss(stoploss_config);

        let lookback_period = std::cmp::max(atr_period, filter.lookback());

        BaseStrategy::new(signal, filter, stop_loss, lookback_period)
    }
}

impl Signals for SNATRStrategy {
    fn id(&self) -> String {
        format!("SNATR_{}:{}", self.atr_period, self.atr_smoothing_period)
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let snatr = snatr(
            &data.high,
            &data.low,
            &data.close,
            self.atr_period,
            self.atr_smoothing_period,
        );

        (snatr.cross_under_line(0.8), snatr.cross_over_line(0.2))
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
