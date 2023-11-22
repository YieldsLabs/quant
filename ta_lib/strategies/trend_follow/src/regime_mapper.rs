use crate::ma_mapper::map_to_ma;
use crate::macd_mapper::map_to_macd;
use crate::rsi_mapper::map_to_rsi;
use crate::stoch_mapper::map_to_stoch;
use base::Regime;
use regime_filter::*;
use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum RegimeConfig {
    Adx {
        adx_period: f32,
        di_period: f32,
        threshold: f32,
    },
    Apo {
        fast_period: f32,
        slow_period: f32,
    },
    Bop {
        signal_smoothing: f32,
    },
    Braid {
        period_one: f32,
        period_two: f32,
        period_three: f32,
        atr_period: f32,
    },
    Fib {
        period: f32,
    },
    Ma {
        smoothing: f32,
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
}

pub fn map_to_regime(config: RegimeConfig) -> Box<dyn Regime> {
    match config {
        RegimeConfig::Apo {
            fast_period,
            slow_period,
        } => Box::new(APOFilter::new(fast_period, slow_period)),
        RegimeConfig::Bop { signal_smoothing } => Box::new(BOPFilter::new(signal_smoothing)),
        RegimeConfig::Ma { smoothing, period } => {
            Box::new(MAFilter::new(map_to_ma(smoothing as usize), period))
        }
        RegimeConfig::Macd {
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
        RegimeConfig::Eis {
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
        RegimeConfig::Rsi {
            rsi_type,
            period,
            threshold,
        } => Box::new(RSIFilter::new(
            map_to_rsi(rsi_type as usize),
            period,
            threshold,
        )),
        RegimeConfig::Ribbon {
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
        RegimeConfig::Stoch {
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
        RegimeConfig::Supertrend { atr_period, factor } => {
            Box::new(SupertrendFilter::new(atr_period, factor))
        }
        RegimeConfig::Adx {
            adx_period,
            di_period,
            threshold,
        } => Box::new(ADXFilter::new(adx_period, di_period, threshold)),
        RegimeConfig::Braid {
            period_one,
            period_two,
            period_three,
            atr_period,
        } => Box::new(BraidFilter::new(
            period_one,
            period_two,
            period_three,
            atr_period,
        )),
        RegimeConfig::Tii {
            major_period,
            minor_period,
            threshold,
        } => Box::new(TIIFilter::new(major_period, minor_period, threshold)),
        RegimeConfig::Dumb { period } => Box::new(DumbFilter::new(period)),
        RegimeConfig::Fib { period } => Box::new(FibFilter::new(period)),
    }
}
