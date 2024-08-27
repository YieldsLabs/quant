use once_cell::sync::Lazy;
use serde::Serialize;
use serde_json::to_string;
use std::collections::HashMap;
use std::sync::atomic::{AtomicI32, Ordering};
use std::sync::{Arc, RwLock};
use timeseries::prelude::*;

type TsTableType = Lazy<Arc<RwLock<HashMap<i32, Box<dyn TimeSeries + Send + Sync + 'static>>>>>;
type Result = (i32, i32);

static TIMESERIES: TsTableType = Lazy::new(|| Arc::new(RwLock::new(HashMap::new())));
static TIMESERIES_ID_COUNTER: Lazy<AtomicI32> = Lazy::new(|| AtomicI32::new(0));

fn generate_timeseries_id() -> i32 {
    TIMESERIES_ID_COUNTER.fetch_add(1, Ordering::SeqCst)
}

const ERROR: Result = (-1, 0);
const NOT_FOUND: Result = (0, 0);

fn serialize<T: Serialize>(data: &T) -> (i32, i32) {
    match to_string(data) {
        Ok(json) => {
            let bytes = json.as_bytes();
            (bytes.as_ptr() as i32, bytes.len() as i32)
        }
        Err(_) => ERROR,
    }
}

#[no_mangle]
pub fn timeseries_register() -> i32 {
    let timeseries_id = generate_timeseries_id();

    let mut timeseries = TIMESERIES.write().unwrap();

    timeseries.insert(timeseries_id, Box::<BaseTimeSeries>::default());

    timeseries_id
}

#[no_mangle]
pub fn timeseries_add(
    timeseries_id: i32,
    ts: i64,
    open: f32,
    high: f32,
    low: f32,
    close: f32,
    volume: f32,
) -> Result {
    let mut timeseries = TIMESERIES.write().unwrap();

    if let Some(timeseries) = timeseries.get_mut(&timeseries_id) {
        let bar = OHLCV {
            ts,
            open,
            high,
            low,
            close,
            volume,
        };

        timeseries.add(&bar);

        NOT_FOUND
    } else {
        ERROR
    }
}

#[no_mangle]
pub fn timeseries_next_bar(
    timeseries_id: i32,
    ts: i64,
    open: f32,
    high: f32,
    low: f32,
    close: f32,
    volume: f32,
) -> Result {
    let timeseries = TIMESERIES.read().unwrap();

    if let Some(timeseries) = timeseries.get(&timeseries_id) {
        let curr_bar = OHLCV {
            ts,
            open,
            high,
            low,
            close,
            volume,
        };

        if let Some(next_bar) = timeseries.next_bar(&curr_bar) {
            serialize(&next_bar)
        } else {
            NOT_FOUND
        }
    } else {
        ERROR
    }
}

#[no_mangle]
pub fn timeseries_prev_bar(
    timeseries_id: i32,
    ts: i64,
    open: f32,
    high: f32,
    low: f32,
    close: f32,
    volume: f32,
) -> Result {
    let timeseries = TIMESERIES.read().unwrap();

    if let Some(timeseries) = timeseries.get(&timeseries_id) {
        let curr_bar = OHLCV {
            ts,
            open,
            high,
            low,
            close,
            volume,
        };

        if let Some(prev_bar) = timeseries.prev_bar(&curr_bar) {
            serialize(&prev_bar)
        } else {
            NOT_FOUND
        }
    } else {
        ERROR
    }
}

#[no_mangle]
pub fn timeseries_back_n_bars(
    timeseries_id: i32,
    ts: i64,
    open: f32,
    high: f32,
    low: f32,
    close: f32,
    volume: f32,
    n: usize,
) -> Result {
    let timeseries = TIMESERIES.read().unwrap();

    if let Some(timeseries) = timeseries.get(&timeseries_id) {
        let curr_bar = OHLCV {
            ts,
            open,
            high,
            low,
            close,
            volume,
        };

        let bars = timeseries.back_n_bars(&curr_bar, n);

        serialize(&bars)
    } else {
        ERROR
    }
}

#[no_mangle]
pub fn timeseries_ta(
    timeseries_id: i32,
    ts: i64,
    open: f32,
    high: f32,
    low: f32,
    close: f32,
    volume: f32,
) -> Result {
    let timeseries = TIMESERIES.read().unwrap();

    if let Some(timeseries) = timeseries.get(&timeseries_id) {
        let curr_bar = OHLCV {
            ts,
            open,
            high,
            low,
            close,
            volume,
        };

        let ta = timeseries.ta(&curr_bar);

        serialize(&ta)
    } else {
        ERROR
    }
}

#[no_mangle]
pub fn timeseries_unregister(timeseries_id: i32) -> i32 {
    let mut timeseries = TIMESERIES.write().unwrap();

    timeseries.remove(&timeseries_id).is_some() as i32
}
