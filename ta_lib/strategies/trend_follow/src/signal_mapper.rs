use crate::candle_mapper::map_to_candle;
use crate::ma_mapper::map_to_ma;
use crate::macd_mapper::map_to_macd;
use crate::rsi_mapper::map_to_rsi;
use base::Signal;
use serde::Deserialize;
use signal::{
    AOFlipSignal, MA3CrossSignal, MACDColorSwitchSignal, MACDCrossSignal, MACDFlipSignal,
    RSI2MASignal, RSINeutralityCrossSignal, RSINeutralityPullbackSignal,
    RSINeutralityRejectionSignal, RSIVSignal, SNATRSignal, SupertrendFlipSignal,
    SupertrendPullBackSignal, TIICrossSignal, TestingGroundSignal, TrendCandleSignal,
};

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum SignalConfig {
    AoFlip {
        short_period: f32,
        long_period: f32,
    },
    Ma3Cross {
        smoothing: f32,
        short_period: f32,
        medium_period: f32,
        long_period: f32,
    },
    MacdFlip {
        macd_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_smoothing: f32,
    },
    MacdCross {
        macd_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_smoothing: f32,
    },
    MacdColorSwitch {
        macd_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_smoothing: f32,
    },
    RsiNeutralityCross {
        rsi_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    RsiNeutralityPullback {
        rsi_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    RsiNeutralityRejection {
        rsi_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    Rsi2Ma {
        rsi_type: f32,
        rsi_period: f32,
        threshold: f32,
        smoothing: f32,
        short_period: f32,
        long_period: f32,
    },
    RsiV {
        rsi_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    TestGround {
        smoothing: f32,
        period: f32,
    },
    TrendCandle {
        candle: f32,
    },
    SnAtr {
        atr_period: f32,
        atr_smoothing_period: f32,
        threshold: f32,
    },
    SupFlip {
        atr_period: f32,
        factor: f32,
    },
    SupPullBack {
        atr_period: f32,
        factor: f32,
    },
    TIICross {
        major_period: f32,
        minor_period: f32,
        threshold: f32,
    },
}

pub fn map_to_signal(config: SignalConfig) -> Box<dyn Signal> {
    match config {
        SignalConfig::AoFlip {
            short_period,
            long_period,
        } => Box::new(AOFlipSignal::new(short_period, long_period)),
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
        SignalConfig::MacdFlip {
            macd_type,
            fast_period,
            slow_period,
            signal_smoothing,
        } => Box::new(MACDFlipSignal::new(
            map_to_macd(macd_type as usize),
            fast_period,
            slow_period,
            signal_smoothing,
        )),
        SignalConfig::MacdCross {
            macd_type,
            fast_period,
            slow_period,
            signal_smoothing,
        } => Box::new(MACDCrossSignal::new(
            map_to_macd(macd_type as usize),
            fast_period,
            slow_period,
            signal_smoothing,
        )),
        SignalConfig::MacdColorSwitch {
            macd_type,
            fast_period,
            slow_period,
            signal_smoothing,
        } => Box::new(MACDColorSwitchSignal::new(
            map_to_macd(macd_type as usize),
            fast_period,
            slow_period,
            signal_smoothing,
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
        SignalConfig::RsiNeutralityPullback {
            rsi_type,
            rsi_period,
            threshold,
        } => Box::new(RSINeutralityPullbackSignal::new(
            map_to_rsi(rsi_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::RsiNeutralityRejection {
            rsi_type,
            rsi_period,
            threshold,
        } => Box::new(RSINeutralityRejectionSignal::new(
            map_to_rsi(rsi_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::Rsi2Ma {
            rsi_type,
            rsi_period,
            threshold,
            smoothing,
            short_period,
            long_period,
        } => Box::new(RSI2MASignal::new(
            map_to_rsi(rsi_type as usize),
            rsi_period,
            threshold,
            map_to_ma(smoothing as usize),
            short_period,
            long_period,
        )),
        SignalConfig::TestGround { smoothing, period } => Box::new(TestingGroundSignal::new(
            map_to_ma(smoothing as usize),
            period,
        )),
        SignalConfig::TrendCandle { candle } => {
            Box::new(TrendCandleSignal::new(map_to_candle(candle as usize)))
        }
        SignalConfig::SnAtr {
            atr_period,
            atr_smoothing_period,
            threshold,
        } => Box::new(SNATRSignal::new(
            atr_period,
            atr_smoothing_period,
            threshold,
        )),
        SignalConfig::SupFlip { atr_period, factor } => {
            Box::new(SupertrendFlipSignal::new(atr_period, factor))
        }
        SignalConfig::SupPullBack { atr_period, factor } => {
            Box::new(SupertrendPullBackSignal::new(atr_period, factor))
        }
        SignalConfig::TIICross {
            major_period,
            minor_period,
            threshold,
        } => Box::new(TIICrossSignal::new(major_period, minor_period, threshold)),
        SignalConfig::RsiV {
            rsi_type,
            rsi_period,
            threshold,
        } => Box::new(RSIVSignal::new(
            map_to_rsi(rsi_type as usize),
            rsi_period,
            threshold,
        )),
    }
}
