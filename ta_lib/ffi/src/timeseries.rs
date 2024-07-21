use once_cell::sync::Lazy;
use serde::Serialize;
use serde_json::to_string;
use std::collections::HashMap;
use std::sync::RwLock;
use timeseries::prelude::*;

static TIMESERIES_ID_TO_INSTANCE: Lazy<
    RwLock<HashMap<i32, Box<dyn TimeSeries + Send + Sync + 'static>>>,
> = Lazy::new(|| RwLock::new(HashMap::new()));

static TIMESERIES_ID_COUNTER: Lazy<RwLock<i32>> = Lazy::new(|| RwLock::new(0));

fn serialize<T: Serialize>(data: &T) -> (i32, i32) {
    match to_string(data) {
        Ok(json) => {
            let bytes = json.as_bytes();
            (bytes.as_ptr() as i32, bytes.len() as i32)
        }
        Err(_) => (-1, 0),
    }
}

#[no_mangle]
pub fn timeseries_register() -> i32 {
    let mut id_counter = TIMESERIES_ID_COUNTER.write().unwrap();
    *id_counter += 1;

    let current_id = *id_counter;

    TIMESERIES_ID_TO_INSTANCE
        .write()
        .unwrap()
        .insert(current_id, Box::<BaseTimeSeries>::default());

    current_id
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
) -> (i32, i32) {
    let mut timeseries = TIMESERIES_ID_TO_INSTANCE.write().unwrap();
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

        (0, 0)
    } else {
        (-1, 0)
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
) -> (i32, i32) {
    let mut timeseries = TIMESERIES_ID_TO_INSTANCE.write().unwrap();
    if let Some(timeseries) = timeseries.get_mut(&timeseries_id) {
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
            (0, 0)
        }
    } else {
        (-1, 0)
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
) -> (i32, i32) {
    let mut timeseries = TIMESERIES_ID_TO_INSTANCE.write().unwrap();
    if let Some(timeseries) = timeseries.get_mut(&timeseries_id) {
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
            (0, 0)
        }
    } else {
        (-1, 0)
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
) -> (i32, i32) {
    let mut timeseries = TIMESERIES_ID_TO_INSTANCE.write().unwrap();
    if let Some(timeseries) = timeseries.get_mut(&timeseries_id) {
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
        (-1, 0)
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
) -> (i32, i32) {
    let mut timeseries = TIMESERIES_ID_TO_INSTANCE.write().unwrap();
    if let Some(timeseries) = timeseries.get_mut(&timeseries_id) {
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
        (-1, 0)
    }
}

#[no_mangle]
pub fn timeseries_unregister(timeseries_id: i32) -> i32 {
    let mut timeseries = TIMESERIES_ID_TO_INSTANCE.write().unwrap();
    timeseries.remove(&timeseries_id).is_some() as i32
}
