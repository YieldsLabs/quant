use crate::CrossMAStrategy;
use base::register_strategy;

#[no_mangle]
pub fn register_crossma(
    smothing: usize,
    short_period: usize,
    long_period: usize,
    atr_period: usize,
    stop_loss_multi: f32,
) -> i32 {
    let ma = match smothing {
        1 => "SMA",
        2 => "EMA",
        3 => "WMA",
        4 => "ZLEMA",
        5 => "HMA",
        6 => "VWMA",
        7 => "DEMA",
        8 => "TEMA",
        _ => "SMA",
    };

    let strategy = CrossMAStrategy::new(
        ma,
        short_period,
        long_period,
        atr_period,
        stop_loss_multi,
    );
    register_strategy(Box::new(strategy))
}
