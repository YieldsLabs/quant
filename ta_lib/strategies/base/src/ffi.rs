use crate::{
    BaseLine, BaseStrategy, Confirm, Exit, Pulse, Signal, StopLoss, Strategy, TradeAction, OHLCV,
};
use once_cell::sync::Lazy;
use std::collections::HashMap;
use std::sync::{Mutex, MutexGuard, RwLock};

static STRATEGY_ID_TO_INSTANCE: Lazy<
    RwLock<HashMap<i32, Box<dyn Strategy + Send + Sync + 'static>>>,
> = Lazy::new(|| RwLock::new(HashMap::new()));

static STRATEGY_ID_COUNTER: Lazy<RwLock<i32>> = Lazy::new(|| RwLock::new(0));

static ALLOC_MUTEX: Lazy<Mutex<()>> = Lazy::new(|| Mutex::new(()));

pub fn register_strategy(
    signal: Box<dyn Signal>,
    confirm: Box<dyn Confirm>,
    pulse: Box<dyn Pulse>,
    base_line: Box<dyn BaseLine>,
    stop_loss: Box<dyn StopLoss>,
    exit: Box<dyn Exit>,
) -> i32 {
    let mut id_counter = STRATEGY_ID_COUNTER.write().unwrap();
    *id_counter += 1;

    let current_id = *id_counter;
    STRATEGY_ID_TO_INSTANCE.write().unwrap().insert(
        current_id,
        Box::new(BaseStrategy::new(
            signal, confirm, pulse, base_line, stop_loss, exit,
        )),
    );

    current_id
}

#[no_mangle]
pub fn unregister_strategy(strategy_id: i32) -> i32 {
    let mut strategies = STRATEGY_ID_TO_INSTANCE.write().unwrap();
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
    let mut strategies = STRATEGY_ID_TO_INSTANCE.write().unwrap();
    if let Some(strategy) = strategies.get_mut(&strategy_id) {
        let ohlcv = OHLCV {
            ts,
            open,
            high,
            low,
            close,
            volume,
        };

        let result = strategy.next(ohlcv);

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
pub fn strategy_stop_loss(strategy_id: i32) -> (f32, f32) {
    let mut strategies = STRATEGY_ID_TO_INSTANCE.write().unwrap();
    if let Some(strategy) = strategies.get_mut(&strategy_id) {
        let stop_loss_levels = strategy.stop_loss();

        (stop_loss_levels.long, stop_loss_levels.short)
    } else {
        (-1.0, -1.0)
    }
}

#[no_mangle]
pub fn allocate(size: usize) -> *mut u8 {
    let _guard: MutexGuard<_> = ALLOC_MUTEX.lock().unwrap();

    let mut buf = Vec::with_capacity(size);
    let ptr = buf.as_mut_ptr();
    std::mem::forget(buf);
    ptr
}
