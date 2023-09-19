use crate::{DumbFilter, MAFilter, RSIFilter};
use base::Filter;
use shared::MovingAverageType;

pub enum FilterConfig {
    MA {
        smoothing: MovingAverageType,
        period: usize,
    },
    RSI {
        period: usize,
        threshold: f32,
    },
    DUMB {},
}

pub fn map_to_filter(config: FilterConfig) -> Box<dyn Filter + Send + Sync> {
    match config {
        FilterConfig::MA { smoothing, period } => Box::new(MAFilter::new(smoothing, period)),
        FilterConfig::RSI { period, threshold } => Box::new(RSIFilter::new(period, threshold)),
        _ => Box::new(DumbFilter::new(55)),
    }
}
