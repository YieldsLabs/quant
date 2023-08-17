use crate::CrossMAStrategy;
use base::register_strategy;

#[no_mangle]
pub fn register_crossma(
    short_period: usize,
    long_period: usize,
    atr_period: usize,
    stop_loss_multi: f32,
) -> i32 {
    let strategy = CrossMAStrategy::new(short_period, long_period, atr_period, stop_loss_multi);
    register_strategy(Box::new(strategy))
}
