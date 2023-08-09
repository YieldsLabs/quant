use base::base::{BaseStrategy, OHLCVSeries, Strategy, StrategySignals};
use core::series::Series;
use std::cmp::max;
use trend::sma::sma;

pub struct MACrossStrategy {
    short_period: usize,
    long_period: usize,
}

impl MACrossStrategy {
    pub fn new(short_period: usize, long_period: usize) -> BaseStrategy<MACrossStrategy> {
        let lookback_period = max(short_period, long_period);
        let strategy = MACrossStrategy {
            short_period,
            long_period,
        };

        BaseStrategy::new(strategy, lookback_period)
    }
}

impl StrategySignals for MACrossStrategy {
    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let short_ma = sma(&data.close, self.short_period);
        let long_ma = sma(&data.close, self.long_period);

        let long_signal = short_ma.cross_over(&long_ma);
        let short_signal = short_ma.cross_under(&long_ma);

        (long_signal, short_signal)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }

    fn parameters(&self) -> Vec<usize> {
        vec![self.short_period, self.long_period]
    }
}

#[no_mangle]
pub extern "C" fn create_macross_strategy(
    short_period: usize,
    long_period: usize,
) -> *mut dyn Strategy {
    let strategy = MACrossStrategy::new(short_period, long_period);
    let boxed_strategy: Box<dyn Strategy> = Box::new(strategy);
    Box::into_raw(boxed_strategy)
}

#[cfg(test)]
mod tests {
    use super::*;
    use base::base::{TradeAction, OHLCV};

    #[test]
    fn test_macrossstrategy_new() {
        let strategy = MACrossStrategy::new(50, 100);
        assert_eq!(strategy.parameters(), vec![50, 100]);
    }

    #[test]
    fn test_macrossstrategy_next_do_nothing() {
        let mut strat = MACrossStrategy::new(50, 100);

        for _i in 0..100 {
            strat.next(OHLCV {
                open: 2.0,
                high: 3.0,
                low: 2.0,
                close: 3.0,
                volume: 2000.0,
            });
        }

        let result = strat.next(OHLCV {
            open: 1.0,
            high: 1.0,
            low: 1.0,
            close: 1.0,
            volume: 20.0,
        });

        assert_eq!(result, TradeAction::DoNothing);
    }
}
