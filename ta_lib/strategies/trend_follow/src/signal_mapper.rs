use base::Signal;
use shared::{MovingAverageType, RSIType, TrendCandleType};
use signal::{
    Cross2MASignal, Cross3MASignal, CrossRSINeutralitySignal, RSI2MASignal, RSIMASignal,
    SNATRSignal, TestingGroundSignal, TrendCandleSignal,
};

pub enum SignalConfig {
    Cross2Ma {
        smoothing: MovingAverageType,
        short_period: f32,
        long_period: f32,
    },
    Cross3Ma {
        smoothing: MovingAverageType,
        short_period: f32,
        medium_period: f32,
        long_period: f32,
    },
    CrossRsiNeutrality {
        rsi_type: RSIType,
        rsi_period: f32,
        threshold: f32,
    },
    RsiMa {
        rsi_type: RSIType,
        rsi_period: f32,
        lower_barrier: f32,
        upper_barrier: f32,
        smoothing: MovingAverageType,
        smoothing_period: f32,
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
}

pub fn map_to_signal(config: SignalConfig) -> Box<dyn Signal> {
    match config {
        SignalConfig::Cross2Ma {
            smoothing,
            short_period,
            long_period,
        } => Box::new(Cross2MASignal::new(smoothing, short_period, long_period)),
        SignalConfig::Cross3Ma {
            smoothing,
            short_period,
            medium_period,
            long_period,
        } => Box::new(Cross3MASignal::new(
            smoothing,
            short_period,
            medium_period,
            long_period,
        )),
        SignalConfig::CrossRsiNeutrality {
            rsi_type,
            rsi_period,
            threshold,
        } => Box::new(CrossRSINeutralitySignal::new(
            rsi_type, rsi_period, threshold,
        )),
        SignalConfig::RsiMa {
            rsi_type,
            rsi_period,
            lower_barrier,
            upper_barrier,
            smoothing,
            smoothing_period,
        } => Box::new(RSIMASignal::new(
            rsi_type,
            rsi_period,
            lower_barrier,
            upper_barrier,
            smoothing,
            smoothing_period,
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
    }
}
