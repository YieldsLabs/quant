use crate::{Strategy, TradeAction, OHLCV};
use once_cell::sync::Lazy;
use std::alloc::Layout;
use std::collections::HashMap;
use std::sync::RwLock;

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

#[no_mangle]
pub fn strategy_stop_loss(strategy_id: i32) -> (f32, f32) {
    let mut strategies = STRATEGY_ID_TO_INSTANCE.write().unwrap();
    if let Some(strategy) = strategies.get_mut(&strategy_id) {
        strategy.stop_loss()
    } else {
        (-1.0, -1.0)
    }
}