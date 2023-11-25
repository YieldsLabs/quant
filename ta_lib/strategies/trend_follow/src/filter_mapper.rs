use crate::ma_mapper::map_to_ma;
use crate::macd_mapper::map_to_macd;
use crate::rsi_mapper::map_to_rsi;
use crate::stoch_mapper::map_to_stoch;
use base::Filter;
use filter::*;
use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum FilterConfig {
    Apo {
        short_period: f32,
        long_period: f32,
    },
    Bop {
        signal_smoothing: f32,
    },
    Braid {
        period_one: f32,
        period_two: f32,
        period_three: f32,
        strength: f32,
        atr_period: f32,
    },
    Dpo {
        period: f32,
    },
    Fib {
        period: f32,
    },
    Macd {
        macd_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_smoothing: f32,
    },
    Eis {
        macd_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_smoothing: f32,
        signal_period: f32,
    },
    Ribbon {
        smoothing: f32,
        first_period: f32,
        second_period: f32,
        third_period: f32,
        fourth_period: f32,
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
    Kst {
        roc_period_first: f32,
        roc_period_second: f32,
        roc_period_third: f32,
        roc_period_fouth: f32,
        period_first: f32,
        period_second: f32,
        period_third: f32,
        period_fouth: f32,
        signal_period: f32,
    },
}

pub fn map_to_filter(config: FilterConfig) -> Box<dyn Filter> {
    match config {
        FilterConfig::Apo {
            short_period,
            long_period,
        } => Box::new(APOFilter::new(short_period, long_period)),
        FilterConfig::Bop { signal_smoothing } => Box::new(BOPFilter::new(signal_smoothing)),
        FilterConfig::Dpo { period } => Box::new(DPOFilter::new(period)),
        FilterConfig::Macd {
            macd_type,
            fast_period,
            slow_period,
            signal_smoothing,
        } => Box::new(MACDFilter::new(
            map_to_macd(macd_type as usize),
            fast_period,
            slow_period,
            signal_smoothing,
        )),
        FilterConfig::Eis {
            macd_type,
            fast_period,
            slow_period,
            signal_smoothing,
            signal_period,
        } => Box::new(EISFilter::new(
            map_to_macd(macd_type as usize),
            fast_period,
            slow_period,
            signal_smoothing,
            signal_period,
        )),
        FilterConfig::Rsi {
            rsi_type,
            period,
            threshold,
        } => Box::new(RSIFilter::new(
            map_to_rsi(rsi_type as usize),
            period,
            threshold,
        )),
        FilterConfig::Ribbon {
            smoothing,
            first_period,
            second_period,
            third_period,
            fourth_period,
        } => Box::new(RibbonFilter::new(
            map_to_ma(smoothing as usize),
            first_period,
            second_period,
            third_period,
            fourth_period,
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
        FilterConfig::Braid {
            period_one,
            period_two,
            period_three,
            strength,
            atr_period,
        } => Box::new(BraidFilter::new(
            period_one,
            period_two,
            period_three,
            strength,
            atr_period,
        )),
        FilterConfig::Tii {
            major_period,
            minor_period,
            threshold,
        } => Box::new(TIIFilter::new(major_period, minor_period, threshold)),
        FilterConfig::Dumb { period } => Box::new(DumbFilter::new(period)),
        FilterConfig::Fib { period } => Box::new(FibFilter::new(period)),
        FilterConfig::Kst {
            roc_period_first,
            roc_period_second,
            roc_period_third,
            roc_period_fouth,
            period_first,
            period_second,
            period_third,
            period_fouth,
            signal_period,
        } => Box::new(KstFilter::new(
            roc_period_first,
            roc_period_second,
            roc_period_third,
            roc_period_fouth,
            period_first,
            period_second,
            period_third,
            period_fouth,
            signal_period,
        )),
    }
}
