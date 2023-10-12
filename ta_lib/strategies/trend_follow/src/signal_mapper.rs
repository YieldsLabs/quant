use crate::candle_mapper::map_to_candle;
use crate::ma_mapper::map_to_ma;
use crate::rsi_mapper::map_to_rsi;
use base::Signal;
use signal::{
    MA3CrossSignal, RSI2MASignal, RSINeutralityCrossSignal, RSIVSignal, SNATRSignal,
    SupertrendFlipSignal, TIICrossSignal, TestingGroundSignal, TrendCandleSignal,
};

pub enum SignalConfig {
    Ma3Cross {
        smoothing: f32,
        short_period: f32,
        medium_period: f32,
        long_period: f32,
    },
    RsiNeutralityCross {
        rsi_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    Rsi2Ma {
        rsi_type: f32,
        rsi_period: f32,
        lower_barrier: f32,
        upper_barrier: f32,
        smoothing: f32,
        short_period: f32,
        long_period: f32,
    },
    RsiV {
        rsi_type: f32,
        rsi_period: f32,
        lower_barrier: f32,
        upper_barrier: f32,
    },
    Testground {
        smoothing: f32,
        smoothing_period: f32,
    },
    Trendcandle {
        candle: f32,
    },
    SnAtr {
        atr_period: f32,
        atr_smoothing_period: f32,
        lower_barrier: f32,
        upper_barrier: f32,
    },
    SupFlip {
        atr_period: f32,
        factor: f32,
    },
    TIICross {
        major_period: f32,
        minor_period: f32,
        lower_barrier: f32,
        upper_barrier: f32,
    },
}

pub fn map_to_signal(config: SignalConfig) -> Box<dyn Signal> {
    match config {
        SignalConfig::Ma3Cross {
            smoothing,
            short_period,
            medium_period,
            long_period,
        } => Box::new(MA3CrossSignal::new(
            map_to_ma(smoothing as usize),
            short_period,
            medium_period,
            long_period,
        )),
        SignalConfig::RsiNeutralityCross {
            rsi_type,
            rsi_period,
            threshold,
        } => Box::new(RSINeutralityCrossSignal::new(
            map_to_rsi(rsi_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::Rsi2Ma {
            rsi_type,
            rsi_period,
            lower_barrier,
            upper_barrier,
            smoothing,
            short_period,
            long_period,
        } => Box::new(RSI2MASignal::new(
            map_to_rsi(rsi_type as usize),
            rsi_period,
            lower_barrier,
            upper_barrier,
            map_to_ma(smoothing as usize),
            short_period,
            long_period,
        )),
        SignalConfig::Testground {
            smoothing,
            smoothing_period,
        } => Box::new(TestingGroundSignal::new(
            map_to_ma(smoothing as usize),
            smoothing_period,
        )),
        SignalConfig::Trendcandle { candle } => {
            Box::new(TrendCandleSignal::new(map_to_candle(candle as usize)))
        }
        SignalConfig::SnAtr {
            atr_period,
            atr_smoothing_period,
            lower_barrier,
            upper_barrier,
        } => Box::new(SNATRSignal::new(
            atr_period,
            atr_smoothing_period,
            lower_barrier,
            upper_barrier,
        )),
        SignalConfig::SupFlip { atr_period, factor } => {
            Box::new(SupertrendFlipSignal::new(atr_period, factor))
        }
        SignalConfig::TIICross {
            major_period,
            minor_period,
            lower_barrier,
            upper_barrier,
        } => Box::new(TIICrossSignal::new(
            major_period,
            minor_period,
            lower_barrier,
            upper_barrier,
        )),
        SignalConfig::RsiV {
            rsi_type,
            rsi_period,
            lower_barrier,
            upper_barrier,
        } => Box::new(RSIVSignal::new(
            map_to_rsi(rsi_type as usize),
            rsi_period,
            lower_barrier,
            upper_barrier,
        )),
    }
}
