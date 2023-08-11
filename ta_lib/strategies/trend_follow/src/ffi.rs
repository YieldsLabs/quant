use crate::CrossMAStrategy;
use base::register_strategy;

#[no_mangle]
pub fn register_crossma(short_period: usize, long_period: usize) -> i32 {
    let strategy = CrossMAStrategy::new(short_period, long_period);
    register_strategy(Box::new(strategy))
}
