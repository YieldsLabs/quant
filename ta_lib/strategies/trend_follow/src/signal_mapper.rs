use base::Signal;
use shared::{MovingAverageType, RSIType, TrendCandleType};
use signal::{
    MA3CrossSignal, RSINeutralityCrossSignal, TIICrossSignal, RSI2MASignal, RSIVSignal,
    SNATRSignal, TestingGroundSignal, TrendCandleSignal,
};

pub enum SignalConfig {
    Ma3Cross {
        smoothing: MovingAverageType,
        short_period: f32,
        medium_period: f32,
        long_period: f32,
    },
    RsiNeutralityCross {
        rsi_type: RSIType,
        rsi_period: f32,
        threshold: f32,
    },
    Rsi2Ma {
        rsi_type: RSIType,
        rsi_period: f32,
        lower_barrier: f32,
        upper_barrier: f32,
        smoothing: MovingAverageType,
        short_period: f32,
        long_period: f32,
    },
    RsiV {
        rsi_type: RSIType,
        rsi_period: f32,
        lower_barrier: f32,
        upper_barrier: f32,
    },
    Testground {
        smoothing: MovingAverageType,
        smoothing_period: f32,
    },
    Trendcandle {
        candle: TrendCandleType,
    },
    SnAtr {
        atr_period: f32,
        atr_smoothing_period: f32,
        lower_barrier: f32,
        upper_barrier: f32,
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
            smoothing,
            short_period,
            medium_period,
            long_period,
        )),
        SignalConfig::RsiNeutralityCross {
            rsi_type,
            rsi_period,
            threshold,
        } => Box::new(RSINeutralityCrossSignal::new(
            rsi_type, rsi_period, threshold,
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
            rsi_type,
            rsi_period,
            lower_barrier,
            upper_barrier,
            smoothing,
            short_period,
            long_period,
        )),
        SignalConfig::Testground {
            smoothing,
            smoothing_period,
        } => Box::new(TestingGroundSignal::new(smoothing, smoothing_period)),
        SignalConfig::Trendcandle { candle } => Box::new(TrendCandleSignal::new(candle)),
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
            rsi_type,
            rsi_period,
            lower_barrier,
            upper_barrier,
        )),
    }
}
