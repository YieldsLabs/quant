use crate::candle_mapper::map_to_candle;
use crate::ma_mapper::map_to_ma;
use crate::macd_mapper::map_to_macd;
use crate::rsi_mapper::map_to_rsi;
use crate::stoch_mapper::map_to_stoch;
use base::Signal;
use serde::Deserialize;
use signal::*;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum SignalConfig {
    AoSaucer {
        short_period: f32,
        long_period: f32,
    },
    AoFlip {
        short_period: f32,
        long_period: f32,
    },
    ApoFlip {
        short_period: f32,
        long_period: f32,
    },
    BopFlip {
        smoothing_period: f32,
    },
    CcFlip {
        short_period: f32,
        long_period: f32,
        smoothing_period: f32,
    },
    DmiCross {
        adx_period: f32,
        di_period: f32,
    },
    HighLow {
        period: f32,
    },
    KstCross {
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
        signal_period: f32,
    },
    MacdCross {
        macd_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    },
    MacdColorSwitch {
        macd_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    },
    RsiNeutralityCross {
        rsi_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    RocFlip {
        period: f32,
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
    RsiMaPullback {
        rsi_type: f32,
        rsi_period: f32,
        smoothing_period: f32,
        threshold: f32,
    },
    DiFlip {
        period: f32,
    },
    DiCross {
        period: f32,
        signal_period: f32,
    },
    Dch2Ma {
        dch_period: f32,
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
    TrixFlip {
        period: f32,
    },
    TrixCross {
        period: f32,
        signal_period: f32,
    },
    SnAtr {
        atr_period: f32,
        atr_smoothing_period: f32,
        threshold: f32,
    },
    StcFlip {
        fast_period: f32,
        slow_period: f32,
        cycle: f32,
        d_first: f32,
        d_second: f32,
    },
    StcUturn {
        fast_period: f32,
        slow_period: f32,
        cycle: f32,
        d_first: f32,
        d_second: f32,
    },
    StochCross {
        stoch_type: f32,
        period: f32,
        k_period: f32,
        d_period: f32,
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
    TiiV {
        major_period: f32,
        minor_period: f32,
    },
    TsiFlip {
        long_period: f32,
        short_period: f32,
    },
    TsiCross {
        long_period: f32,
        short_period: f32,
        signal_period: f32,
    },
    QstickFlip {
        period: f32,
    },
    QstickCross {
        period: f32,
        signal_period: f32,
    },
    Quadruple {
        smoothing: f32,
        period: f32,
    },
    VwapCross {
        period: f32,
    },
}

pub fn map_to_signal(config: SignalConfig) -> Box<dyn Signal> {
    match config {
        SignalConfig::AoFlip {
            short_period,
            long_period,
        } => Box::new(AOFlipSignal::new(short_period, long_period)),
        SignalConfig::AoSaucer {
            short_period,
            long_period,
        } => Box::new(AOSaucerSignal::new(short_period, long_period)),
        SignalConfig::ApoFlip {
            short_period,
            long_period,
        } => Box::new(APOFlipSignal::new(short_period, long_period)),
        SignalConfig::BopFlip { smoothing_period } => {
            Box::new(BOPFlipSignal::new(smoothing_period))
        }
        SignalConfig::CcFlip {
            short_period,
            long_period,
            smoothing_period,
        } => Box::new(CCFlipSignal::new(
            short_period,
            long_period,
            smoothing_period,
        )),
        SignalConfig::DmiCross {
            adx_period,
            di_period,
        } => Box::new(DMICrossSignal::new(adx_period, di_period)),
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
            signal_period,
        } => Box::new(MACDFlipSignal::new(
            map_to_macd(macd_type as usize),
            fast_period,
            slow_period,
            signal_period,
        )),
        SignalConfig::MacdCross {
            macd_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(MACDCrossSignal::new(
            map_to_macd(macd_type as usize),
            fast_period,
            slow_period,
            signal_period,
        )),
        SignalConfig::MacdColorSwitch {
            macd_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(MACDColorSwitchSignal::new(
            map_to_macd(macd_type as usize),
            fast_period,
            slow_period,
            signal_period,
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
        SignalConfig::RsiMaPullback {
            rsi_type,
            rsi_period,
            smoothing_period,
            threshold,
        } => Box::new(RSIMaPullbackSignal::new(
            map_to_rsi(rsi_type as usize),
            rsi_period,
            smoothing_period,
            threshold,
        )),
        SignalConfig::DiFlip { period } => Box::new(DIFlipSignal::new(period)),
        SignalConfig::DiCross {
            period,
            signal_period,
        } => Box::new(DICrossSignal::new(period, signal_period)),
        SignalConfig::HighLow { period } => Box::new(HighLowSignal::new(period)),
        SignalConfig::Dch2Ma {
            dch_period,
            smoothing,
            short_period,
            long_period,
        } => Box::new(DCH2MASignal::new(
            dch_period,
            map_to_ma(smoothing as usize),
            short_period,
            long_period,
        )),
        SignalConfig::RocFlip { period } => Box::new(ROCFlipSignal::new(period)),
        SignalConfig::TestGround { smoothing, period } => Box::new(TestingGroundSignal::new(
            map_to_ma(smoothing as usize),
            period,
        )),
        SignalConfig::TrendCandle { candle } => {
            Box::new(TrendCandleSignal::new(map_to_candle(candle as usize)))
        }
        SignalConfig::TrixFlip { period } => Box::new(TRIXFlipSignal::new(period)),
        SignalConfig::TrixCross {
            period,
            signal_period,
        } => Box::new(TRIXCrossSignal::new(period, signal_period)),
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
        SignalConfig::StcFlip {
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        } => Box::new(STCFlipSignal::new(
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        )),
        SignalConfig::StcUturn {
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        } => Box::new(STCUturnSignal::new(
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        )),
        SignalConfig::StochCross {
            stoch_type,
            period,
            k_period,
            d_period,
        } => Box::new(StochCrossSignal::new(
            map_to_stoch(stoch_type as usize),
            period,
            k_period,
            d_period,
        )),
        SignalConfig::TIICross {
            major_period,
            minor_period,
            threshold,
        } => Box::new(TIICrossSignal::new(major_period, minor_period, threshold)),
        SignalConfig::TiiV {
            major_period,
            minor_period,
        } => Box::new(TIIVSignal::new(major_period, minor_period)),
        SignalConfig::RsiV {
            rsi_type,
            rsi_period,
            threshold,
        } => Box::new(RSIVSignal::new(
            map_to_rsi(rsi_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::TsiFlip {
            long_period,
            short_period,
        } => Box::new(TSIFlipSignal::new(long_period, short_period)),
        SignalConfig::TsiCross {
            long_period,
            short_period,
            signal_period,
        } => Box::new(TSICrossSignal::new(
            long_period,
            short_period,
            signal_period,
        )),
        SignalConfig::QstickFlip { period } => Box::new(QSTICKFlipSignal::new(period)),
        SignalConfig::QstickCross {
            period,
            signal_period,
        } => Box::new(QSTICKCrossSignal::new(period, signal_period)),
        SignalConfig::Quadruple { smoothing, period } => {
            Box::new(QuadrupleSignal::new(map_to_ma(smoothing as usize), period))
        }
        SignalConfig::VwapCross { period } => Box::new(VWAPCrossSignal::new(period)),
        SignalConfig::KstCross {
            roc_period_first,
            roc_period_second,
            roc_period_third,
            roc_period_fouth,
            period_first,
            period_second,
            period_third,
            period_fouth,
            signal_period,
        } => Box::new(KSTCrossSignal::new(
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
