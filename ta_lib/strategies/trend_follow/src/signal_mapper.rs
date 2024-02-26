use crate::candle_mapper::map_to_candle;
use crate::ma_mapper::map_to_ma;
use crate::smooth_mapper::map_to_smooth;
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
        smooth_type: f32,
        smoothing_period: f32,
    },
    CfoFlip {
        period: f32,
    },
    CcFlip {
        short_period: f32,
        long_period: f32,
        smooth_type: f32,
        smoothing_period: f32,
    },
    DmiCross {
        smooth_type: f32,
        adx_period: f32,
        di_period: f32,
    },
    HighLow {
        period: f32,
    },
    KstCross {
        smooth_type: f32,
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
        ma: f32,
        short_period: f32,
        medium_period: f32,
        long_period: f32,
    },
    MacdFlip {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    },
    MacdCross {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    },
    MacdColorSwitch {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    },
    MacdBb {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
        bb_period: f32,
        factor: f32,
    },
    RocFlip {
        period: f32,
    },
    RsiNeutralityCross {
        smooth_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    RsiNeutralityPullback {
        smooth_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    RsiNeutralityRejection {
        smooth_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    Rsi2Ma {
        smooth_type: f32,
        rsi_period: f32,
        threshold: f32,
        ma: f32,
        short_period: f32,
        long_period: f32,
    },
    RsiSup {
        smooth_type: f32,
        rsi_period: f32,
        threshold: f32,
        atr_period: f32,
        factor: f32,
    },
    RsiMaPullback {
        smooth_type: f32,
        rsi_period: f32,
        smooth_signal: f32,
        smoothing_period: f32,
        threshold: f32,
    },
    RsiV {
        smooth_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    DiFlip {
        smooth_type: f32,
        period: f32,
    },
    DiCross {
        smooth_type: f32,
        period: f32,
        signal_period: f32,
    },
    Dch2Ma {
        dch_period: f32,
        ma: f32,
        short_period: f32,
        long_period: f32,
    },
    TestGround {
        ma: f32,
        period: f32,
    },
    TrendCandle {
        candle: f32,
    },
    TrixFlip {
        smooth_type: f32,
        period: f32,
    },
    TrixCross {
        smooth_type: f32,
        period: f32,
        signal_period: f32,
    },
    SnAtr {
        smooth_type: f32,
        atr_period: f32,
        atr_smoothing_period: f32,
        threshold: f32,
    },
    StcFlip {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        cycle: f32,
        d_first: f32,
        d_second: f32,
    },
    StochCross {
        smooth_type: f32,
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
    TiiCross {
        smooth_type: f32,
        major_period: f32,
        minor_period: f32,
        threshold: f32,
    },
    TiiV {
        smooth_type: f32,
        major_period: f32,
        minor_period: f32,
    },
    TsiFlip {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
    },
    TsiCross {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    },
    QstickFlip {
        smooth_type: f32,
        period: f32,
    },
    QstickCross {
        smooth_type: f32,
        period: f32,
        signal_period: f32,
    },
    Quadruple {
        ma: f32,
        period: f32,
    },
    ViCross {
        atr_period: f32,
        period: f32,
    },
    VwapCross {
        period: f32,
    },
    VwapBb {
        period: f32,
        smooth_type: f32,
        bb_period: f32,
        factor: f32,
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
        SignalConfig::BopFlip {
            smooth_type,
            smoothing_period,
        } => Box::new(BOPFlipSignal::new(
            map_to_smooth(smooth_type as usize),
            smoothing_period,
        )),
        SignalConfig::CfoFlip { period } => Box::new(CFOFlipSignal::new(period)),
        SignalConfig::CcFlip {
            short_period,
            long_period,
            smooth_type,
            smoothing_period,
        } => Box::new(CCFlipSignal::new(
            short_period,
            long_period,
            map_to_smooth(smooth_type as usize),
            smoothing_period,
        )),
        SignalConfig::DmiCross {
            smooth_type,
            adx_period,
            di_period,
        } => Box::new(DMICrossSignal::new(
            map_to_smooth(smooth_type as usize),
            adx_period,
            di_period,
        )),
        SignalConfig::Ma3Cross {
            ma,
            short_period,
            medium_period,
            long_period,
        } => Box::new(MA3CrossSignal::new(
            map_to_ma(ma as usize),
            short_period,
            medium_period,
            long_period,
        )),
        SignalConfig::MacdFlip {
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(MACDFlipSignal::new(
            map_to_smooth(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
        )),
        SignalConfig::MacdCross {
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(MACDCrossSignal::new(
            map_to_smooth(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
        )),
        SignalConfig::MacdColorSwitch {
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(MACDColorSwitchSignal::new(
            map_to_smooth(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
        )),
        SignalConfig::MacdBb {
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
            bb_period,
            factor,
        } => Box::new(MACDBBSignal::new(
            map_to_smooth(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
            bb_period,
            factor,
        )),
        SignalConfig::RsiNeutralityCross {
            smooth_type,
            rsi_period,
            threshold,
        } => Box::new(RSINeutralityCrossSignal::new(
            map_to_smooth(smooth_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::RsiNeutralityPullback {
            smooth_type,
            rsi_period,
            threshold,
        } => Box::new(RSINeutralityPullbackSignal::new(
            map_to_smooth(smooth_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::RsiNeutralityRejection {
            smooth_type,
            rsi_period,
            threshold,
        } => Box::new(RSINeutralityRejectionSignal::new(
            map_to_smooth(smooth_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::Rsi2Ma {
            smooth_type,
            rsi_period,
            threshold,
            ma,
            short_period,
            long_period,
        } => Box::new(RSI2MASignal::new(
            map_to_smooth(smooth_type as usize),
            rsi_period,
            threshold,
            map_to_ma(ma as usize),
            short_period,
            long_period,
        )),
        SignalConfig::RsiSup {
            smooth_type,
            rsi_period,
            threshold,
            atr_period,
            factor,
        } => Box::new(RSISupertrendSignal::new(
            map_to_smooth(smooth_type as usize),
            rsi_period,
            threshold,
            atr_period,
            factor,
        )),
        SignalConfig::RsiMaPullback {
            smooth_type,
            rsi_period,
            smooth_signal,
            smoothing_period,
            threshold,
        } => Box::new(RSIMaPullbackSignal::new(
            map_to_smooth(smooth_type as usize),
            rsi_period,
            map_to_smooth(smooth_signal as usize),
            smoothing_period,
            threshold,
        )),
        SignalConfig::DiFlip {
            smooth_type,
            period,
        } => Box::new(DIFlipSignal::new(
            map_to_smooth(smooth_type as usize),
            period,
        )),
        SignalConfig::DiCross {
            smooth_type,
            period,
            signal_period,
        } => Box::new(DICrossSignal::new(
            map_to_smooth(smooth_type as usize),
            period,
            signal_period,
        )),
        SignalConfig::HighLow { period } => Box::new(HighLowSignal::new(period)),
        SignalConfig::Dch2Ma {
            dch_period,
            ma,
            short_period,
            long_period,
        } => Box::new(DCH2MASignal::new(
            dch_period,
            map_to_ma(ma as usize),
            short_period,
            long_period,
        )),
        SignalConfig::RocFlip { period } => Box::new(ROCFlipSignal::new(period)),
        SignalConfig::TestGround { ma, period } => {
            Box::new(TestingGroundSignal::new(map_to_ma(ma as usize), period))
        }
        SignalConfig::TrendCandle { candle } => {
            Box::new(TrendCandleSignal::new(map_to_candle(candle as usize)))
        }
        SignalConfig::TrixFlip {
            smooth_type,
            period,
        } => Box::new(TRIXFlipSignal::new(
            map_to_smooth(smooth_type as usize),
            period,
        )),
        SignalConfig::TrixCross {
            smooth_type,
            period,
            signal_period,
        } => Box::new(TRIXCrossSignal::new(
            map_to_smooth(smooth_type as usize),
            period,
            signal_period,
        )),
        SignalConfig::SnAtr {
            smooth_type,
            atr_period,
            atr_smoothing_period,
            threshold,
        } => Box::new(SNATRSignal::new(
            map_to_smooth(smooth_type as usize),
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
            smooth_type,
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        } => Box::new(STCFlipSignal::new(
            map_to_smooth(smooth_type as usize),
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        )),
        SignalConfig::StochCross {
            smooth_type,
            period,
            k_period,
            d_period,
        } => Box::new(StochCrossSignal::new(
            map_to_smooth(smooth_type as usize),
            period,
            k_period,
            d_period,
        )),
        SignalConfig::TiiCross {
            smooth_type,
            major_period,
            minor_period,
            threshold,
        } => Box::new(TIICrossSignal::new(
            map_to_smooth(smooth_type as usize),
            major_period,
            minor_period,
            threshold,
        )),
        SignalConfig::TiiV {
            smooth_type,
            major_period,
            minor_period,
        } => Box::new(TIIVSignal::new(
            map_to_smooth(smooth_type as usize),
            major_period,
            minor_period,
        )),
        SignalConfig::RsiV {
            smooth_type,
            rsi_period,
            threshold,
        } => Box::new(RSIVSignal::new(
            map_to_smooth(smooth_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::TsiFlip {
            smooth_type,
            fast_period,
            slow_period,
        } => Box::new(TSIFlipSignal::new(
            map_to_smooth(smooth_type as usize),
            fast_period,
            slow_period,
        )),
        SignalConfig::TsiCross {
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(TSICrossSignal::new(
            map_to_smooth(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
        )),
        SignalConfig::QstickFlip {
            smooth_type,
            period,
        } => Box::new(QSTICKFlipSignal::new(
            map_to_smooth(smooth_type as usize),
            period,
        )),
        SignalConfig::QstickCross {
            smooth_type,
            period,
            signal_period,
        } => Box::new(QSTICKCrossSignal::new(
            map_to_smooth(smooth_type as usize),
            period,
            signal_period,
        )),
        SignalConfig::Quadruple { ma, period } => {
            Box::new(QuadrupleSignal::new(map_to_ma(ma as usize), period))
        }
        SignalConfig::ViCross { period, atr_period } => {
            Box::new(VICrossSignal::new(period, atr_period))
        }
        SignalConfig::VwapCross { period } => Box::new(VWAPCrossSignal::new(period)),
        SignalConfig::VwapBb {
            period,
            smooth_type,
            bb_period,
            factor,
        } => Box::new(VWAPBBSignal::new(
            period,
            map_to_smooth(smooth_type as usize),
            bb_period,
            factor,
        )),
        SignalConfig::KstCross {
            smooth_type,
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
            map_to_smooth(smooth_type as usize),
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
