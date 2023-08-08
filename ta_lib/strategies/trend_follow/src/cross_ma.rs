use base::base::{BaseStrategy, OHLCVSeries, Strategy, TradeAction, OHLCV};
use core::series::Series;
use std::cmp::max;
use std::collections::HashMap;
use trend::sma::sma;

pub struct MACrossStrategy {
    base: BaseStrategy,
    short_period: usize,
    long_period: usize,
}

impl MACrossStrategy {
    pub fn new(short_period: usize, long_period: usize) -> Self {
        let lookback_period = max(short_period, long_period);

        MACrossStrategy {
            base: BaseStrategy::new(lookback_period),
            short_period,
            long_period,
        }
    }
}

impl Strategy for MACrossStrategy {
    fn next(&mut self, data: OHLCV) -> TradeAction {
        self.base.next(data)
    }

    fn can_process(&self) -> bool {
        self.base.can_process()
    }

    fn params(&self) -> HashMap<String, usize> {
        let mut map = self.base.params();
        map.insert(String::from("short_period"), self.short_period);
        map.insert(String::from("long_period"), self.long_period);
        map
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let short_ma = sma(&data.close, self.short_period);
        let long_ma = sma(&data.close, self.long_period);

        let long_signal = short_ma.cross_over(&long_ma);
        let short_signal = short_ma.cross_under(&long_ma);

        (long_signal, short_signal)
    }

    fn exit(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        self.base.exit(data)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_macrossstrategy_new() {
        let strat = MACrossStrategy::new(50, 100);
        assert_eq!(strat.short_period, 50);
        assert_eq!(strat.long_period, 100);
    }

    #[test]
    fn test_macrossstrategy_params() {
        let strat = MACrossStrategy::new(50, 100);
        let params = strat.params();
        assert_eq!(params.get("lookback_period"), Some(&100));
        assert_eq!(params.get("short_period"), Some(&50));
        assert_eq!(params.get("long_period"), Some(&100));
    }
}
