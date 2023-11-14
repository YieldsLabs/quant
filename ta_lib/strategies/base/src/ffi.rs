use crate::{BaseStrategy, Exit, Regime, Signal, StopLoss, Strategy, TradeAction, Volume, OHLCV};
use once_cell::sync::Lazy;
use std::collections::HashMap;
use std::sync::RwLock;

static STRATEGY_ID_TO_INSTANCE: Lazy<
    RwLock<HashMap<i32, Box<dyn Strategy + Send + Sync + 'static>>>,
> = Lazy::new(|| RwLock::new(HashMap::new()));

static STRATEGY_ID_COUNTER: Lazy<RwLock<i32>> = Lazy::new(|| RwLock::new(0));

pub fn register_strategy(
    signal: Box<dyn Signal>,
    regime: Box<dyn Regime>,
    volume: Box<dyn Volume>,
    stop_loss: Box<dyn StopLoss>,
    exit: Box<dyn Exit>,
) -> i32 {
    let mut id_counter = STRATEGY_ID_COUNTER.write().unwrap();
    *id_counter += 1;

    let current_id = *id_counter;
    STRATEGY_ID_TO_INSTANCE.write().unwrap().insert(
        current_id,
        Box::new(BaseStrategy::new(signal, regime, volume, stop_loss, exit)),
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
        let stop_loss_levels = strategy.stop_loss();

        (stop_loss_levels.long, stop_loss_levels.short)
    } else {
        (-1.0, -1.0)
    }
}

#[no_mangle]
pub fn allocate(size: usize) -> *mut u8 {
    let mut buf = vec![0; size];
    buf.resize(size, 0);
    let ptr = buf.as_mut_ptr();
    std::mem::forget(buf);
    ptr
}
