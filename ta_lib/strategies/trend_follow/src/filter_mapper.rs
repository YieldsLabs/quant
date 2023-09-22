use base::Filter;
use filter::{DumbFilter, MAFilter, RSIFilter};
use shared::{MovingAverageType, RSIType};

pub enum FilterConfig {
    Ma {
        smoothing: MovingAverageType,
        period: f32,
    },
    Rsi {
        rsi_type: RSIType,
        period: f32,
        threshold: f32,
    },
    Dumb {
        period: f32,
    },
}

pub fn map_to_filter(config: FilterConfig) -> Box<dyn Filter> {
    match config {
        FilterConfig::Ma { smoothing, period } => Box::new(MAFilter::new(smoothing, period)),
        FilterConfig::Rsi {
            rsi_type,
            period,
            threshold,
        } => Box::new(RSIFilter::new(rsi_type, period, threshold)),
        FilterConfig::Dumb { period } => Box::new(DumbFilter::new(period)),
    }
}
