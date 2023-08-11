use base::{BaseStrategy, OHLCVSeries, StrategySignals};
use core::series::Series;
use trend::sma::sma;

pub struct CrossMAStrategy {
    short_period: usize,
    long_period: usize,
}

impl CrossMAStrategy {
    pub fn new(short_period: usize, long_period: usize) -> BaseStrategy<CrossMAStrategy> {
        let lookback_period = std::cmp::max(short_period, long_period);
        let strategy = CrossMAStrategy {
            short_period,
            long_period,
        };

        BaseStrategy::new(strategy, lookback_period)
    }
}

impl StrategySignals for CrossMAStrategy {
    fn signal_id(&self) -> String {
        format!("CROSSMA_{}_{}", self.short_period, self.long_period)
    }

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
}

#[cfg(test)]
mod tests {
    use super::*;
    use base::{TradeAction, TradingStrategy, OHLCV};

    #[test]
    fn test_crossmatrategy_new() {
        let strategy = CrossMAStrategy::new(50, 100);
        assert_eq!(strategy.strategy_id(), "_STRTGCROSSMA_50_100");
    }

    #[test]
    fn test_crossmastrategy_next_do_nothing() {
        let mut strat = CrossMAStrategy::new(50, 100);

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
