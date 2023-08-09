use core::series::Series;
use price::{average::average_price, median::median_price, typical::typical_price, wcl::wcl};
use std::{cmp::max, collections::VecDeque};

const DEFAULT_LOOKBACK: usize = 55;

#[derive(Debug, Clone, Copy)]
pub struct OHLCV {
    pub open: f32,
    pub high: f32,
    pub low: f32,
    pub close: f32,
    pub volume: f32,
}

pub struct OHLCVSeries {
    pub open: Vec<f32>,
    pub high: Vec<f32>,
    pub low: Vec<f32>,
    pub close: Vec<f32>,
    pub volume: Vec<f32>,
}

impl OHLCVSeries {
    fn new(data: &VecDeque<OHLCV>) -> OHLCVSeries {
        OHLCVSeries {
            open: data.iter().map(|ohlcv| ohlcv.open).collect(),
            high: data.iter().map(|ohlcv| ohlcv.high).collect(),
            low: data.iter().map(|ohlcv| ohlcv.low).collect(),
            close: data.iter().map(|ohlcv| ohlcv.close).collect(),
            volume: data.iter().map(|ohlcv| ohlcv.volume).collect(),
        }
    }
}

trait Price {
    fn hl2(&self) -> Vec<f32>;
    fn hlc3(&self) -> Vec<f32>;
    fn hlcc4(&self) -> Vec<f32>;
    fn ohlc4(&self) -> Vec<f32>;
}

impl Price for OHLCVSeries {
    fn hl2(&self) -> Vec<f32> {
        median_price(&self.high, &self.low)
    }

    fn hlc3(&self) -> Vec<f32> {
        typical_price(&self.high, &self.low, &self.close)
    }

    fn hlcc4(&self) -> Vec<f32> {
        wcl(&self.high, &self.low, &self.close)
    }

    fn ohlc4(&self) -> Vec<f32> {
        average_price(&self.open, &self.high, &self.low, &self.close)
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum TradeAction {
    GoLong(f32),
    GoShort(f32),
    ExitLong,
    ExitShort,
    DoNothing,
}

impl Default for TradeAction {
    fn default() -> Self {
        TradeAction::DoNothing
    }
}

pub trait StrategySignals {
    fn parameters(&self) -> Vec<usize>;
    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
    fn exit(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait Strategy {
    fn parameters(&self) -> Vec<usize>;
    fn next(&mut self, data: OHLCV) -> TradeAction;
}

pub struct BaseStrategy<S: StrategySignals> {
    data: VecDeque<OHLCV>,
    strategy: S,
    lookback_period: usize,
}

impl<S: StrategySignals> BaseStrategy<S> {
    pub fn new(strategy: S, lookback_period: usize) -> BaseStrategy<S> {
        let lookback_period = max(lookback_period, DEFAULT_LOOKBACK);

        BaseStrategy {
            data: VecDeque::with_capacity(lookback_period),
            strategy,
            lookback_period,
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

impl<S: StrategySignals> Strategy for BaseStrategy<S> {
    fn next(&mut self, data: OHLCV) -> TradeAction {
        self.store(data);

        if !self.can_process() {
            return TradeAction::default();
        }

        let series = OHLCVSeries::new(&self.data);

        let (go_long_series, go_short_series) = self.strategy.entry(&series);
        let (exit_long_series, exit_short_series) = self.strategy.exit(&series);

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
            _ => TradeAction::default(),
        }
    }

    fn parameters(&self) -> Vec<usize> {
        self.strategy.parameters()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

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

        fn parameters(&self) -> Vec<usize> {
            vec![self.short_period]
        }
    }

    #[test]
    fn test_base_strategy_lookback() {
        let strategy = BaseStrategy::<DumbStrategy>::new(DumbStrategy { short_period: 10 }, 2);
        assert_eq!(strategy.lookback_period, 55);
    }

    #[test]
    fn test_base_strategy_parameters() {
        let strategy = BaseStrategy::<DumbStrategy>::new(DumbStrategy { short_period: 10 }, 2);
        assert_eq!(strategy.parameters(), vec![10]);
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

        let series = OHLCVSeries::new(&strategy.data);

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
