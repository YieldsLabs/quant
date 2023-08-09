use crate::base::{Strategy, TradeAction, OHLCV};

#[no_mangle]
pub extern "C" fn strategy_next(ptr: *mut dyn Strategy, data: OHLCV) -> TradeAction {
    assert!(!ptr.is_null());
    let strategy = unsafe { &mut *ptr };
    strategy.next(data)
}

#[no_mangle]
pub extern "C" fn strategy_parameters(ptr: *mut dyn Strategy) -> *mut Vec<usize> {
    assert!(!ptr.is_null());
    let strategy = unsafe { &mut *ptr };
    Box::into_raw(Box::new(strategy.parameters()))
}

#[no_mangle]
pub extern "C" fn strategy_free(ptr: *mut dyn Strategy) {
    if ptr.is_null() {
        return;
    }

    unsafe {
        let _ = Box::from_raw(ptr);
    }
}
