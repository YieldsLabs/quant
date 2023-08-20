use base::{BaseStrategy, OHLCVSeries, Signals};
use core::series::Series;
use stop_loss::ATRStopLoss;
use trend::sma::sma;

pub struct CrossMAStrategy {
    short_period: usize,
    long_period: usize,
}

impl CrossMAStrategy {
    pub fn new(
        short_period: usize,
        long_period: usize,
        atr_period: usize,
        stop_loss_multi: f32,
    ) -> BaseStrategy<CrossMAStrategy, ATRStopLoss> {
        let lookback_period = std::cmp::max(short_period, long_period);
        let signal = CrossMAStrategy {
            short_period,
            long_period,
        };

        let stop_loss = ATRStopLoss {
            atr_period,
            multi: stop_loss_multi,
        };

        BaseStrategy::new(signal, stop_loss, lookback_period)
    }
}

impl Signals for CrossMAStrategy {
    fn id(&self) -> String {
        format!("CROSSMA_{}:{}", self.short_period, self.long_period)
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
    use base::{Strategy, TradeAction, OHLCV};

    #[test]
    fn test_crossmatrategy_new() {
        let strategy = CrossMAStrategy::new(50, 100, 14, 2.0);
        assert_eq!(strategy.id(), "_STRTGCROSSMA_50:100_STPLSSATR_14:2.0");
    }

    #[test]
    fn test_crossmastrategy_next_do_nothing() {
        let mut strat = CrossMAStrategy::new(50, 100, 14, 2.0);

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
