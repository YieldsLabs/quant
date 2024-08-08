use crate::{
    BaseLine, BaseStrategy, Confirm, Exit, Pulse, Signal, StopLoss, Strategy, TradeAction,
};
use once_cell::sync::Lazy;
use std::collections::HashMap;
use std::sync::atomic::{AtomicI32, Ordering};
use std::sync::{Arc, RwLock};
use timeseries::prelude::*;

static STRATEGIES: Lazy<Arc<RwLock<HashMap<i32, Box<dyn Strategy + Send + Sync + 'static>>>>> =
    Lazy::new(|| Arc::new(RwLock::new(HashMap::new())));

static STRATEGIES_ID_COUNTER: Lazy<AtomicI32> = Lazy::new(|| AtomicI32::new(0));

fn generate_strategy_id() -> i32 {
    STRATEGIES_ID_COUNTER.fetch_add(1, Ordering::SeqCst)
}

pub fn register_strategy(
    timeseries: Box<dyn TimeSeries>,
    signal: Box<dyn Signal>,
    confirm: Box<dyn Confirm>,
    pulse: Box<dyn Pulse>,
    base_line: Box<dyn BaseLine>,
    stop_loss: Box<dyn StopLoss>,
    exit: Box<dyn Exit>,
) -> i32 {
    let strategy_id = generate_strategy_id();

    let strategy = Box::new(BaseStrategy::new(
        timeseries,
        signal,
        confirm,
        pulse,
        base_line,
        stop_loss,
        exit,
    ));

    let mut strategies = STRATEGIES.write().unwrap();

    strategies.insert(strategy_id, strategy);

    strategy_id
}

#[no_mangle]
pub fn unregister_strategy(strategy_id: i32) -> i32 {
    let mut strategies = STRATEGIES.write().unwrap();
    strategies.remove(&strategy_id).is_some() as i32
}

#[no_mangle]
pub fn strategy_next(
    strategy_id: i32,
    ts: i64,
    open: f32,
    high: f32,
    low: f32,
    close: f32,
    volume: f32,
) -> (i32, f32) {
    let mut strategies = STRATEGIES.write().unwrap();
    if let Some(strategy) = strategies.get_mut(&strategy_id) {
        let bar = OHLCV {
            ts,
            open,
            high,
            low,
            close,
            volume,
        };

        let result = strategy.next(&bar);

        match result {
            TradeAction::GoLong(entry_price) => (1, entry_price),
            TradeAction::GoShort(entry_price) => (2, entry_price),
            TradeAction::ExitLong(exit_price) => (3, exit_price),
            TradeAction::ExitShort(exit_price) => (4, exit_price),
            TradeAction::DoNothing => (0, 0.0),
        }
    } else {
        (-1, 0.0)
    }
}

#[no_mangle]
pub fn strategy_stop_loss(
    strategy_id: i32,
    ts: i64,
    open: f32,
    high: f32,
    low: f32,
    close: f32,
    volume: f32,
) -> (f32, f32) {
    let strategies = STRATEGIES.read().unwrap();

    if let Some(strategy) = strategies.get(&strategy_id) {
        let bar = OHLCV {
            ts,
            open,
            high,
            low,
            close,
            volume,
        };
        let stop_loss_levels = strategy.stop_loss(&bar);
        (stop_loss_levels.long, stop_loss_levels.short)
    } else {
        (-1.0, -1.0)
    }
}

#[no_mangle]
pub fn allocate(size: usize) -> *mut u8 {
    let mut buf = Vec::with_capacity(size);
    let ptr = buf.as_mut_ptr();
    std::mem::forget(buf);
    ptr
}

#[cfg(test)]
mod tests {
    use super::*;
    use core::prelude::*;

    const period: usize = 7;

    struct MockSignal;
    impl Signal for MockSignal {
        fn lookback(&self) -> usize {
            period
        }

        fn trigger(&self, bar: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = bar.len();
            (Series::one(len).into(), Series::zero(len).into())
        }
    }

    struct MockConfirm;
    impl Confirm for MockConfirm {
        fn lookback(&self) -> usize {
            period
        }

        fn filter(&self, bar: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = bar.len();
            (Series::one(len).into(), Series::zero(len).into())
        }
    }

    struct MockPulse;
    impl Pulse for MockPulse {
        fn lookback(&self) -> usize {
            period
        }

        fn assess(&self, bar: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = bar.len();
            (Series::one(len).into(), Series::zero(len).into())
        }
    }

    struct MockBaseLine;
    impl BaseLine for MockBaseLine {
        fn lookback(&self) -> usize {
            period
        }

        fn filter(&self, bar: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = bar.len();
            (Series::one(len).into(), Series::zero(len).into())
        }

        fn close(&self, bar: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = bar.len();
            (Series::zero(len).into(), Series::zero(len).into())
        }
    }

    struct MockStopLoss;
    impl StopLoss for MockStopLoss {
        fn lookback(&self) -> usize {
            period
        }

        fn find(&self, bar: &OHLCVSeries) -> (Series<f32>, Series<f32>) {
            let len = bar.len();
            (Series::zero(len), Series::zero(len))
        }
    }

    struct MockExit;
    impl Exit for MockExit {
        fn lookback(&self) -> usize {
            period
        }

        fn close(&self, bar: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = bar.len();
            (Series::zero(len).into(), Series::zero(len).into())
        }
    }

    #[test]
    fn test_register_strategy() {
        let timeseries = Box::<BaseTimeSeries>::default();
        let signal = Box::new(MockSignal);
        let primary_confirm = Box::new(MockConfirm);
        let secondary_confirm = Box::new(MockConfirm);
        let pulse = Box::new(MockPulse);
        let base_line = Box::new(MockBaseLine);
        let stop_loss = Box::new(MockStopLoss);
        let exit = Box::new(MockExit);

        let strategy_id = register_strategy(
            timeseries,
            signal,
            primary_confirm,
            secondary_confirm,
            pulse,
            base_line,
            stop_loss,
            exit,
        );

        assert!(strategy_id >= 0);
    }

    #[test]
    fn test_unregister_strategy() {
        let timeseries = Box::<BaseTimeSeries>::default();
        let signal = Box::new(MockSignal);
        let primary_confirm = Box::new(MockConfirm);
        let secondary_confirm = Box::new(MockConfirm);
        let pulse = Box::new(MockPulse);
        let base_line = Box::new(MockBaseLine);
        let stop_loss = Box::new(MockStopLoss);
        let exit = Box::new(MockExit);

        let strategy_id = register_strategy(
            timeseries,
            signal,
            primary_confirm,
            secondary_confirm,
            pulse,
            base_line,
            stop_loss,
            exit,
        );

        assert_eq!(unregister_strategy(strategy_id), 1);
    }

    #[test]
    fn test_strategy_next() {
        let timeseries = Box::<BaseTimeSeries>::default();
        let signal = Box::new(MockSignal);
        let primary_confirm = Box::new(MockConfirm);
        let secondary_confirm = Box::new(MockConfirm);
        let pulse = Box::new(MockPulse);
        let base_line = Box::new(MockBaseLine);
        let stop_loss = Box::new(MockStopLoss);
        let exit = Box::new(MockExit);
        let ohlcv: Vec<OHLCV> = vec![
            OHLCV {
                ts: 1722710400876,
                open: 0.29098,
                high: 0.29309,
                low: 0.29062,
                close: 0.29215,
                volume: 241728.0,
            },
            OHLCV {
                ts: 1722710700876,
                open: 0.29215,
                high: 0.2933,
                low: 0.29193,
                close: 0.29239,
                volume: 88614.0,
            },
            OHLCV {
                ts: 1722711000877,
                open: 0.29239,
                high: 0.29256,
                low: 0.28962,
                close: 0.28982,
                volume: 162963.0,
            },
            OHLCV {
                ts: 1722711300876,
                open: 0.28982,
                high: 0.2903,
                low: 0.28909,
                close: 0.28939,
                volume: 201946.0,
            },
            OHLCV {
                ts: 1722711600883,
                open: 0.28939,
                high: 0.2911,
                low: 0.28926,
                close: 0.2911,
                volume: 162808.0,
            },
            OHLCV {
                ts: 1722711900876,
                open: 0.2911,
                high: 0.29201,
                low: 0.2897,
                close: 0.29057,
                volume: 170885.0,
            },
            OHLCV {
                ts: 1722712200876,
                open: 0.29057,
                high: 0.2918,
                low: 0.28919,
                close: 0.29152,
                volume: 172555.0,
            },
            OHLCV {
                ts: 1722712500877,
                open: 0.29152,
                high: 0.29212,
                low: 0.29027,
                close: 0.29027,
                volume: 101626.0,
            },
            OHLCV {
                ts: 1722712800876,
                open: 0.29027,
                high: 0.29029,
                low: 0.28891,
                close: 0.29026,
                volume: 181359.0,
            },
            OHLCV {
                ts: 1722713100877,
                open: 0.29026,
                high: 0.29133,
                low: 0.28933,
                close: 0.29085,
                volume: 79674.0,
            },
            OHLCV {
                ts: 1722713400876,
                open: 0.29085,
                high: 0.29111,
                low: 0.28844,
                close: 0.28854,
                volume: 157827.0,
            },
            OHLCV {
                ts: 1722713700878,
                open: 0.28854,
                high: 0.29161,
                low: 0.28852,
                close: 0.29103,
                volume: 213401.0,
            },
            OHLCV {
                ts: 1722714000876,
                open: 0.29103,
                high: 0.29145,
                low: 0.29007,
                close: 0.29025,
                volume: 89210.0,
            },
            OHLCV {
                ts: 1722714300876,
                open: 0.29025,
                high: 0.29166,
                low: 0.29005,
                close: 0.29123,
                volume: 80272.0,
            },
            OHLCV {
                ts: 1722714600876,
                open: 0.29123,
                high: 0.29235,
                low: 0.29051,
                close: 0.29082,
                volume: 315809.0,
            },
            OHLCV {
                ts: 1722714300876,
                open: 0.29025,
                high: 0.29166,
                low: 0.29005,
                close: 0.29123,
                volume: 80272.0,
            },
            OHLCV {
                ts: 1722714900876,
                open: 0.29082,
                high: 0.29196,
                low: 0.28921,
                close: 0.28935,
                volume: 190734.0,
            },
            OHLCV {
                ts: 1722715200876,
                open: 0.28935,
                high: 0.28994,
                low: 0.28853,
                close: 0.28854,
                volume: 249121.0,
            },
            OHLCV {
                ts: 1722716100876,
                open: 0.288,
                high: 0.29089,
                low: 0.28766,
                close: 0.2902,
                volume: 100654.0,
            },
            OHLCV {
                ts: 1722715500877,
                open: 0.28854,
                high: 0.28924,
                low: 0.28808,
                close: 0.28915,
                volume: 465408.0,
            },
            OHLCV {
                ts: 1722715800876,
                open: 0.28915,
                high: 0.28954,
                low: 0.28712,
                close: 0.288,
                volume: 218446.0,
            },
        ];

        let strategy_id = register_strategy(
            timeseries,
            signal,
            primary_confirm,
            secondary_confirm,
            pulse,
            base_line,
            stop_loss,
            exit,
        );

        let mut res = vec![];
        for bar in &ohlcv {
            let (action, _) = strategy_next(
                strategy_id,
                bar.ts,
                bar.open,
                bar.high,
                bar.low,
                bar.close,
                bar.volume,
            );
            res.push(action);
        }

        assert_eq!(res.len(), ohlcv.len());
        assert_eq!(res[res.len() - 1], 1);
    }
}
