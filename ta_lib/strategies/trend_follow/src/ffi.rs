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
        1 => "ALMA",
        2 => "DEMA",
        3 => "EMA",
        4 => "FRAMA",
        5 => "GMA",
        6 => "HMA",
        7 => "RMSMA",
        8 => "SMA",
        9 => "SMMA",
        10 => "T3",
        11 => "TEMA",
        12 => "TMA",
        13 => "VWMA",
        14 => "WMA",
        15 => "ZLEMA",
        _ => "SMA",
    };

    let strategy = CrossMAStrategy::new(ma, short_period, long_period, atr_period, stop_loss_multi);
    register_strategy(Box::new(strategy))
}
