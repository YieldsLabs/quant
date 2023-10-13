use crate::ma_mapper::map_to_ma;
use crate::rsi_mapper::map_to_rsi;
use base::Filter;
use filter::{ADXFilter, DumbFilter, MAFilter, RSIFilter};

const DEFAULT_LOOKBACK: f32 = 13.0;

pub enum FilterConfig {
    Adx {
        smoothing_period: f32,
        di_period: f32,
        atr_period: f32,
        threshold: f32,
    },
    Ma {
        smoothing: f32,
        period: f32,
    },
    Rsi {
        rsi_type: f32,
        period: f32,
        threshold: f32,
    },
    Dumb {
        period: f32,
    },
}

pub fn map_to_filter(config: FilterConfig) -> Box<dyn Filter> {
    match config {
        FilterConfig::Ma { smoothing, period } => {
            Box::new(MAFilter::new(map_to_ma(smoothing as usize), period))
        }
        FilterConfig::Rsi {
            rsi_type,
            period,
            threshold,
        } => Box::new(RSIFilter::new(
            map_to_rsi(rsi_type as usize),
            period,
            threshold,
        )),
        FilterConfig::Adx {
            smoothing_period,
            di_period,
            atr_period,
            threshold,
        } => Box::new(ADXFilter::new(
            smoothing_period,
            di_period,
            atr_period,
            threshold,
        )),
        FilterConfig::Dumb { period } => Box::new(DumbFilter::new(period)),
        _ => Box::new(DumbFilter::new(DEFAULT_LOOKBACK)),
    }
}
