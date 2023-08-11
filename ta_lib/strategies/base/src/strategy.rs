use crate::model::OHLCV;
use crate::price::Price;
use crate::OHLCVSeries;
use core::series::Series;
use std::collections::VecDeque;

const DEFAULT_LOOKBACK: usize = 55;

#[derive(Debug, PartialEq)]
pub enum TradeAction {
    GoLong(f32),
    GoShort(f32),
    ExitLong,
    ExitShort,
    DoNothing,
}

pub trait StrategySignals {
    fn signal_id(&self) -> String;
    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
    fn exit(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait TradingStrategy {
    fn strategy_id(&self) -> String;
    fn next(&mut self, ohlcv: OHLCV) -> TradeAction;
}

pub struct BaseStrategy<S: StrategySignals> {
    data: VecDeque<OHLCV>,
    signal: S,
    lookback_period: usize,
}

impl<S: StrategySignals> BaseStrategy<S> {
    pub fn new(signal: S, lookback_period: usize) -> Self {
        let adjusted_lookback = std::cmp::max(lookback_period, DEFAULT_LOOKBACK);

        Self {
            data: VecDeque::with_capacity(adjusted_lookback),
            lookback_period: adjusted_lookback,
            signal,
        }
    }

    fn store(&mut self, data: OHLCV) {
        self.data.push_back(data);

        if self.data.len() > self.lookback_period {
            self.data.pop_front();
        }
    }

    fn can_process(&self) -> bool {
        self.data.len() >= self.lookback_period
    }
}

impl<S: StrategySignals> TradingStrategy for BaseStrategy<S> {
    fn next(&mut self, data: OHLCV) -> TradeAction {
        self.store(data);

        if !self.can_process() {
            return TradeAction::DoNothing;
        }

        let series = OHLCVSeries::from_data(&self.data);

        let (go_long_series, go_short_series) = self.signal.entry(&series);
        let (exit_long_series, exit_short_series) = self.signal.exit(&series);

        let go_long = go_long_series
            .into_iter()
            .flatten()
            .last()
            .unwrap_or_default();
        let go_short = go_short_series
            .into_iter()
            .flatten()
            .last()
            .unwrap_or_default();
        let exit_long = exit_long_series
            .into_iter()
            .flatten()
            .last()
            .unwrap_or_default();
        let exit_short = exit_short_series
            .into_iter()
            .flatten()
            .last()
            .unwrap_or_default();

        let suggested_entry = series.hlc3().last().unwrap_or(&std::f32::NAN).clone();

        match (go_long, go_short, exit_long, exit_short) {
            (true, _, _, _) => TradeAction::GoLong(suggested_entry),
            (_, true, _, _) => TradeAction::GoShort(suggested_entry),
            (_, _, true, _) => TradeAction::ExitLong,
            (_, _, _, true) => TradeAction::ExitShort,
            _ => TradeAction::DoNothing,
        }
    }

    fn strategy_id(&self) -> String {
        format!("_STRTG{}", self.signal.signal_id())
    }
}

#[cfg(test)]
mod tests {
    use crate::price::Price;
    use crate::strategy::TradingStrategy;
    use crate::{BaseStrategy, OHLCVSeries, StrategySignals, OHLCV};
    use core::series::Series;

    struct DumbStrategy {
        short_period: usize,
    }

    impl StrategySignals for DumbStrategy {
        fn entry(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            (Series::empty(1), Series::empty(1))
        }

        fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            (Series::empty(1), Series::empty(1))
        }

        fn signal_id(&self) -> String {
            format!("DUMB_{}", self.short_period)
        }
    }

    #[test]
    fn test_base_strategy_lookback() {
        let strategy = BaseStrategy::<DumbStrategy>::new(DumbStrategy { short_period: 10 }, 2);
        assert_eq!(strategy.lookback_period, 55);
    }

    #[test]
    fn test_base_strategy_id() {
        let strategy = BaseStrategy::<DumbStrategy>::new(DumbStrategy { short_period: 10 }, 2);
        assert_eq!(strategy.strategy_id(), "_STRTGDUMB_10");
    }

    #[test]
    fn test_strategy_data() {
        let mut strategy = BaseStrategy::new(DumbStrategy { short_period: 10 }, 3);
        let ohlcvs = vec![
            OHLCV {
                open: 1.0,
                high: 2.0,
                low: 0.5,
                close: 1.5,
                volume: 100.0,
            },
            OHLCV {
                open: 2.0,
                high: 3.0,
                low: 1.5,
                close: 2.5,
                volume: 200.0,
            },
            OHLCV {
                open: 3.0,
                high: 4.0,
                low: 2.5,
                close: 3.5,
                volume: 300.0,
            },
            OHLCV {
                open: 4.0,
                high: 5.0,
                low: 3.5,
                close: 4.5,
                volume: 400.0,
            },
        ];

        for ohlcv in ohlcvs {
            strategy.next(ohlcv);
        }

        let series = OHLCVSeries::from_data(&strategy.data);

        assert_eq!(series.open, vec![1.0, 2.0, 3.0, 4.0]);
        assert_eq!(series.high, vec![2.0, 3.0, 4.0, 5.0]);
        assert_eq!(series.low, vec![0.5, 1.5, 2.5, 3.5]);
        assert_eq!(series.close, vec![1.5, 2.5, 3.5, 4.5]);
        assert_eq!(series.volume, vec![100.0, 200.0, 300.0, 400.0]);

        assert_eq!(series.hl2(), vec![1.25, 2.25, 3.25, 4.25]);
        assert_eq!(
            series.hlc3(),
            vec![
                1.3333333333333333,
                2.3333333333333335,
                3.3333333333333335,
                4.333333333333333
            ]
        );
        assert_eq!(series.hlcc4(), vec![1.375, 2.375, 3.375, 4.375]);
        assert_eq!(series.ohlc4(), vec![1.25, 2.25, 3.25, 4.25]);
    }
}
