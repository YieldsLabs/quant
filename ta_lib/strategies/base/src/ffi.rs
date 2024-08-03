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
    primary_confirm: Box<dyn Confirm>,
    secondary_confirm: Box<dyn Confirm>,
    pulse: Box<dyn Pulse>,
    base_line: Box<dyn BaseLine>,
    stop_loss: Box<dyn StopLoss>,
    exit: Box<dyn Exit>,
) -> i32 {
    let strategy_id = generate_strategy_id();

    let strategy = Box::new(BaseStrategy::new(
        timeseries,
        signal,
        primary_confirm,
        secondary_confirm,
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
    let bar = OHLCV {
        ts,
        open,
        high,
        low,
        close,
        volume,
    };

    let mut strategies = STRATEGIES.write().unwrap();
    if let Some(strategy) = strategies.get_mut(&strategy_id) {
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
pub fn strategy_stop_loss(strategy_id: i32) -> (f32, f32) {
    let strategies = STRATEGIES.read().unwrap();

    if let Some(strategy) = strategies.get(&strategy_id) {
        let stop_loss_levels = strategy.stop_loss();
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
