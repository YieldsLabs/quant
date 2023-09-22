use base::Signal;
use shared::{MovingAverageType, RSIType, TrendCandleType};
use signal::{
    Cross2xMASignal, Cross3xMASignal, RSI2xMASignal, RSIMASignal, SNATRSignal, TestingGroundSignal,
    TrendCandleSignal,
};

pub enum SignalConfig {
    Cross2xMa {
        smoothing: MovingAverageType,
        short_period: f32,
        long_period: f32,
    },
    Cross3xMa {
        smoothing: MovingAverageType,
        short_period: f32,
        medium_period: f32,
        long_period: f32,
    },
    RsiMa {
        rsi_type: RSIType,
        rsi_period: f32,
        lower_barrier: f32,
        upper_barrier: f32,
        smoothing: MovingAverageType,
        smoothing_period: f32,
    },
    Rsi2xMa {
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
        SignalConfig::Cross2xMa {
            smoothing,
            short_period,
            long_period,
        } => Box::new(Cross2xMASignal::new(smoothing, short_period, long_period)),
        SignalConfig::Cross3xMa {
            smoothing,
            short_period,
            medium_period,
            long_period,
        } => Box::new(Cross3xMASignal::new(
            smoothing,
            short_period,
            medium_period,
            long_period,
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
        SignalConfig::Rsi2xMa {
            rsi_type,
            rsi_period,
            lower_barrier,
            upper_barrier,
            smoothing,
            short_period,
            long_period,
        } => Box::new(RSI2xMASignal::new(
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
