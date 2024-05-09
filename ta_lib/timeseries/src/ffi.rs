use crate::{TimeSeries, OHLCV};
use once_cell::sync::Lazy;
use std::collections::HashMap;
use std::sync::RwLock;

static TIMESERIES_ID_TO_INSTANCE: Lazy<RwLock<HashMap<i32, Box<TimeSeries>>>> =
    Lazy::new(|| RwLock::new(HashMap::new()));

static ID_COUNTER: Lazy<RwLock<i32>> = Lazy::new(|| RwLock::new(0));

fn read_from_memory(ptr: *const u8, len: usize) -> &'static [u8] {
    unsafe { std::slice::from_raw_parts(ptr, len) }
}

#[no_mangle]
pub fn register_timeseries() -> i32 {
    let mut id_counter = ID_COUNTER.write().unwrap();
    *id_counter += 1;

    let current_id = *id_counter;

    TIMESERIES_ID_TO_INSTANCE
        .write()
        .unwrap()
        .insert(current_id, Box::new(TimeSeries::new()));

    current_id
}

#[no_mangle]
pub fn next_bar(timeseries_id: i32, curr_ptr: *const u8, curr_len: usize) -> (i32, i32) {
    let mut timeseries = TIMESERIES_ID_TO_INSTANCE.write().unwrap();
    if let Some(timeseries) = timeseries.get_mut(&timeseries_id) {
        let curr_bar_buffer = read_from_memory(curr_ptr, curr_len);
        let curr_bar: OHLCV = serde_json::from_slice(curr_bar_buffer).unwrap();

        if let Some(next_bar) = timeseries.next_bar(&curr_bar) {
            let next_bar_ptr = &next_bar as *const _ as i32;
            let next_bar_len = std::mem::size_of_val(&next_bar) as i32;

            (next_bar_ptr, next_bar_len)
        } else {
            (0, 0)
        }
    } else {
        (-1, 0)
    }
}
