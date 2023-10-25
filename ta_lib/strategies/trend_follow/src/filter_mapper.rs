use crate::ma_mapper::map_to_ma;
use crate::rsi_mapper::map_to_rsi;
use crate::stoch_mapper::map_to_stoch;
use base::Filter;
use filter::{
    ADXFilter, DumbFilter, MAFilter, RSIFilter, StochFilter, SupertrendFilter, TIIFilter,
};
use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum FilterConfig {
    Adx {
        adx_period: f32,
        di_period: f32,
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
    Stoch {
        stoch_type: f32,
        period: f32,
        k_period: f32,
        d_period: f32,
    },
    Supertrend {
        atr_period: f32,
        factor: f32,
    },
    Tii {
        major_period: f32,
        minor_period: f32,
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
        FilterConfig::Stoch {
            stoch_type,
            period,
            k_period,
            d_period,
        } => Box::new(StochFilter::new(
            map_to_stoch(stoch_type as usize),
            period,
            k_period,
            d_period,
        )),
        FilterConfig::Supertrend { atr_period, factor } => {
            Box::new(SupertrendFilter::new(atr_period, factor))
        }
        FilterConfig::Adx {
            adx_period,
            di_period,
            threshold,
        } => Box::new(ADXFilter::new(adx_period, di_period, threshold)),
        FilterConfig::Tii {
            major_period,
            minor_period,
            threshold,
        } => Box::new(TIIFilter::new(major_period, minor_period, threshold)),
        FilterConfig::Dumb { period } => Box::new(DumbFilter::new(period)),
    }
}
