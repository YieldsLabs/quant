#![feature(alloc)]
extern crate alloc;
use core::series::Series;
use once_cell::sync::Lazy;
use price::{average::average_price, median::median_price, typical::typical_price, wcl::wcl};
use std::alloc::Layout;
use std::collections::HashMap;
use std::collections::VecDeque;
use std::sync::RwLock;

const DEFAULT_LOOKBACK: usize = 55;

#[derive(Debug, Copy, Clone)]
pub struct OHLCV {
    pub open: f32,
    pub high: f32,
    pub low: f32,
    pub close: f32,
    pub volume: f32,
}

#[derive(Debug, Clone)]
pub struct OHLCVSeries {
    pub open: Vec<f32>,
    pub high: Vec<f32>,
    pub low: Vec<f32>,
    pub close: Vec<f32>,
    pub volume: Vec<f32>,
}

impl OHLCVSeries {
    fn from_data(data: &VecDeque<OHLCV>) -> Self {
        let len = data.len();

        let mut open = Vec::with_capacity(len);
        let mut high = Vec::with_capacity(len);
        let mut low = Vec::with_capacity(len);
        let mut close = Vec::with_capacity(len);
        let mut volume = Vec::with_capacity(len);

        for ohlcv in data.iter() {
            open.push(ohlcv.open);
            high.push(ohlcv.high);
            low.push(ohlcv.low);
            close.push(ohlcv.close);
            volume.push(ohlcv.volume);
        }

        Self {
            open,
            high,
            low,
            close,
            volume,
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

#[derive(Debug, PartialEq)]
pub enum TradeAction {
    GoLong(f32),
    GoShort(f32),
    ExitLong,
    ExitShort,
    DoNothing,
}

pub trait StrategySignals {
    fn id(&self) -> String;
    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
    fn exit(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait Strategy {
    fn next(&mut self, ohlcv: OHLCV) -> TradeAction;
    fn id(&self) -> String;
}

pub struct BaseStrategy<S: StrategySignals> {
    data: VecDeque<OHLCV>,
    strategy: S,
    lookback_period: usize,
}

impl<S: StrategySignals> BaseStrategy<S> {
    pub fn new(strategy: S, lookback_period: usize) -> Self {
        let adjusted_lookback = std::cmp::max(lookback_period, DEFAULT_LOOKBACK);

        Self {
            data: VecDeque::with_capacity(adjusted_lookback),
            lookback_period: adjusted_lookback,
            strategy,
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
            return TradeAction::DoNothing;
        }

        let series = OHLCVSeries::from_data(&self.data);

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
            _ => TradeAction::DoNothing,
        }
    }

    fn id(&self) -> String {
        format!("_STRTG{}", self.strategy.id())
    }
}

static STRATEGY_ID_TO_INSTANCE: Lazy<
    RwLock<HashMap<i32, Box<dyn Strategy + Send + Sync + 'static>>>,
> = Lazy::new(|| RwLock::new(HashMap::new()));

static STRATEGY_ID_COUNTER: Lazy<RwLock<i32>> = Lazy::new(|| RwLock::new(0));

pub fn register_strategy(strategy: Box<dyn Strategy + Send + Sync + 'static>) -> i32 {
    let mut id_counter = STRATEGY_ID_COUNTER.write().unwrap();
    *id_counter += 1;

    let current_id = *id_counter;
    STRATEGY_ID_TO_INSTANCE
        .write()
        .unwrap()
        .insert(current_id, strategy);

    current_id
}

#[no_mangle]
pub fn unregister_strategy(strategy_id: i32) -> i32 {
    let mut strategies = STRATEGY_ID_TO_INSTANCE.write().unwrap();
    strategies.remove(&strategy_id).is_some() as i32
}

#[no_mangle]
pub fn strategy_parameters(strategy_id: i32) -> (i32, i32) {
    let strategies = STRATEGY_ID_TO_INSTANCE.read().unwrap();
    if let Some(strategy) = strategies.get(&strategy_id) {
        let id = strategy.id();

        let bytes = id.as_bytes();

        let result_ptr = unsafe {
            let ptr = alloc::alloc::alloc(Layout::from_size_align(bytes.len(), 1).unwrap());
            ptr.copy_from_nonoverlapping(bytes.as_ptr(), bytes.len());
            ptr as i32
        };

        (result_ptr, bytes.len() as i32)
    } else {
        (-1, -1)
    }
}

#[no_mangle]
pub fn strategy_next(
    strategy_id: i32,
    open: f32,
    high: f32,
    low: f32,
    close: f32,
    volume: f32,
) -> (f32, f32) {
    let mut strategies = STRATEGY_ID_TO_INSTANCE.write().unwrap();
    if let Some(strategy) = strategies.get_mut(&strategy_id) {
        let ohlcv = OHLCV {
            open,
            high,
            low,
            close,
            volume,
        };

        let result = strategy.next(ohlcv);

        match result {
            TradeAction::GoLong(price) => (1.0, price),
            TradeAction::GoShort(price) => (2.0, price),
            TradeAction::ExitLong => (3.0, 0.0),
            TradeAction::ExitShort => (4.0, 0.0),
            TradeAction::DoNothing => (0.0, 0.0),
        }
    } else {
        (-1.0, 0.0)
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

        fn id(&self) -> String {
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
        assert_eq!(strategy.id(), "_STRTGDUMB_10");
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
