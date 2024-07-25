use crate::config::SignalConfig;
use crate::deserialize::{
    candlereversal_deserialize, candletrend_deserialize, ma_deserialize, smooth_deserialize,
    source_deserialize,
};
use base::prelude::*;
use signal::*;

#[inline]
pub fn map_to_signal(config: SignalConfig) -> Box<dyn Signal> {
    match config {
        // Zero Cross
        SignalConfig::AoZeroCross {
            source_type,
            smooth_type,
            fast_period,
            slow_period,
        } => Box::new(AoZeroCrossSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
        )),
        SignalConfig::BopZeroCross {
            smooth_type,
            smooth_period,
        } => Box::new(BopZeroCrossSignal::new(
            smooth_deserialize(smooth_type as usize),
            smooth_period,
        )),
        SignalConfig::CfoZeroCross {
            source_type,
            period,
        } => Box::new(CfoZeroCrossSignal::new(
            source_deserialize(source_type as usize),
            period,
        )),
        SignalConfig::CcZeroCross {
            source_type,
            fast_period,
            slow_period,
            smooth_type,
            smooth_period,
        } => Box::new(CcZeroCrossSignal::new(
            source_deserialize(source_type as usize),
            fast_period,
            slow_period,
            smooth_deserialize(smooth_type as usize),
            smooth_period,
        )),
        SignalConfig::DiZeroCross {
            source_type,
            smooth_type,
            period,
        } => Box::new(DiZeroCrossSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
        )),
        SignalConfig::MacdZeroCross {
            source_type,
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(MacdZeroCrossSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
        )),
        SignalConfig::RocZeroCross {
            source_type,
            period,
        } => Box::new(RocZeroCrossSignal::new(
            source_deserialize(source_type as usize),
            period,
        )),
        SignalConfig::TsiZeroCross {
            source_type,
            smooth_type,
            fast_period,
            slow_period,
        } => Box::new(TsiZeroCrossSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
        )),
        SignalConfig::TrixZeroCross {
            source_type,
            smooth_type,
            period,
        } => Box::new(TrixZeroCrossSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
        )),
        SignalConfig::QstickZeroCross {
            smooth_type,
            period,
        } => Box::new(QstickZeroCrossSignal::new(
            smooth_deserialize(smooth_type as usize),
            period,
        )),
        // Signal Line
        SignalConfig::MacdSignalLine {
            source_type,
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(MacdSignalLineSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
        )),
        SignalConfig::RsiSignalLine {
            source_type,
            smooth_type,
            rsi_period,
            smooth_signal,
            smooth_period,
            threshold,
        } => Box::new(RsiSignalLineSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            rsi_period,
            smooth_deserialize(smooth_signal as usize),
            smooth_period,
            threshold,
        )),
        SignalConfig::DsoSignalLine {
            source_type,
            smooth_type,
            smooth_period,
            k_period,
            d_period,
        } => Box::new(DsoSignalLineSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            smooth_period,
            k_period,
            d_period,
        )),
        SignalConfig::TrixSignalLine {
            source_type,
            smooth_type,
            period,
            signal_period,
        } => Box::new(TrixSignalLineSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
            signal_period,
        )),
        SignalConfig::KstSignalLine {
            source_type,
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
        } => Box::new(KstSignalLineSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
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
        SignalConfig::DiSignalLine {
            source_type,
            smooth_type,
            period,
            signal_period,
        } => Box::new(DiSignalLineSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
            signal_period,
        )),
        SignalConfig::TsiSignalLine {
            source_type,
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(TsiSignalLineSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
        )),
        SignalConfig::QstickSignalLine {
            smooth_type,
            period,
            signal_period,
        } => Box::new(QstickSignalLineSignal::new(
            smooth_deserialize(smooth_type as usize),
            period,
            signal_period,
        )),
        SignalConfig::StochSignalLine {
            smooth_type,
            period,
            k_period,
            d_period,
        } => Box::new(StochSignalLineSignal::new(
            smooth_deserialize(smooth_type as usize),
            period,
            k_period,
            d_period,
        )),
        // Flip
        SignalConfig::CeFlip {
            source_type,
            period,
            smooth_atr,
            period_atr,
            factor,
        } => Box::new(CeFlipSignal::new(
            source_deserialize(source_type as usize),
            period,
            smooth_deserialize(smooth_atr as usize),
            period_atr,
            factor,
        )),
        SignalConfig::SupFlip {
            source_type,
            smooth_atr,
            period_atr,
            factor,
        } => Box::new(SupertrendFlipSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_atr as usize),
            period_atr,
            factor,
        )),
        // Pattern
        SignalConfig::AoSaucer {
            source_type,
            smooth_type,
            fast_period,
            slow_period,
        } => Box::new(AoSaucerSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
        )),
        SignalConfig::HighLow { period } => Box::new(HighLowSignal::new(period)),
        SignalConfig::CandlestickTrend { candle } => Box::new(CandlestickTrendSignal::new(
            candletrend_deserialize(candle as usize),
        )),
        SignalConfig::CandlestickReversal { candle } => Box::new(CandlestickReversalSignal::new(
            candlereversal_deserialize(candle as usize),
        )),
        // Color Switch
        SignalConfig::MacdColorSwitch {
            source_type,
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(MacdColorSwitchSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
        )),
        // Contrarian
        SignalConfig::Snatr {
            smooth_type,
            atr_period,
            atr_smooth_period,
            threshold,
        } => Box::new(SnatrSignal::new(
            smooth_deserialize(smooth_type as usize),
            atr_period,
            atr_smooth_period,
            threshold,
        )),
        SignalConfig::TiiV {
            source,
            smooth,
            major_period,
            minor_period,
        } => Box::new(TiiVSignal::new(
            source_deserialize(source as usize),
            smooth_deserialize(smooth as usize),
            major_period,
            minor_period,
        )),
        SignalConfig::StochE {
            source,
            smooth,
            period,
            period_k,
            period_d,
            threshold,
        } => Box::new(StochESignal::new(
            source_deserialize(source as usize),
            smooth_deserialize(smooth as usize),
            period,
            period_k,
            period_d,
            threshold,
        )),
        SignalConfig::RsiC {
            source,
            smooth,
            period,
            threshold,
        } => Box::new(RsiCSignal::new(
            source_deserialize(source as usize),
            smooth_deserialize(smooth as usize),
            period,
            threshold,
        )),
        SignalConfig::RsiD {
            source,
            smooth,
            period,
            threshold,
        } => Box::new(RsiDSignal::new(
            source_deserialize(source as usize),
            smooth_deserialize(smooth as usize),
            period,
            threshold,
        )),
        SignalConfig::RsiNt {
            source,
            smooth,
            period,
            threshold,
        } => Box::new(RsiNtSignal::new(
            source_deserialize(source as usize),
            smooth_deserialize(smooth as usize),
            period,
            threshold,
        )),
        SignalConfig::RsiU {
            source,
            smooth,
            period,
            threshold,
        } => Box::new(RsiUSignal::new(
            source_deserialize(source as usize),
            smooth_deserialize(smooth as usize),
            period,
            threshold,
        )),
        SignalConfig::RsiV {
            source,
            smooth,
            period,
            threshold,
        } => Box::new(RsiVSignal::new(
            source_deserialize(source as usize),
            smooth_deserialize(smooth as usize),
            period,
            threshold,
        )),
        // BB
        SignalConfig::MacdBb {
            source_type,
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
            bb_smooth,
            bb_period,
            factor,
        } => Box::new(MacdBbSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
            smooth_deserialize(bb_smooth as usize),
            bb_period,
            factor,
        )),
        SignalConfig::VwapBb {
            source_type,
            period,
            bb_smooth,
            bb_period,
            factor,
        } => Box::new(VwapBbSignal::new(
            source_deserialize(source_type as usize),
            period,
            smooth_deserialize(bb_smooth as usize),
            bb_period,
            factor,
        )),
        // Neutrality
        SignalConfig::RsiNeutralityCross {
            source_type,
            smooth_type,
            rsi_period,
            threshold,
        } => Box::new(RsiNeutralityCrossSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::RsiNeutralityPullback {
            source_type,
            smooth_type,
            rsi_period,
            threshold,
        } => Box::new(RsiNeutralityPullbackSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::RsiNeutralityRejection {
            source_type,
            smooth_type,
            rsi_period,
            threshold,
        } => Box::new(RsiNeutralityRejectionSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::DsoNeutralityCross {
            source_type,
            smooth_type,
            smooth_period,
            k_period,
            d_period,
        } => Box::new(DsoNeutralityCrossSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            smooth_period,
            k_period,
            d_period,
        )),
        SignalConfig::TiiNeutralityCross {
            source_type,
            smooth_type,
            major_period,
            minor_period,
        } => Box::new(TiiNeutralityCrossSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            major_period,
            minor_period,
        )),
        // Ma
        SignalConfig::Ma3Cross {
            source_type,
            ma,
            fast_period,
            medium_period,
            slow_period,
        } => Box::new(Ma3CrossSignal::new(
            source_deserialize(source_type as usize),
            ma_deserialize(ma as usize),
            fast_period,
            medium_period,
            slow_period,
        )),
        SignalConfig::Ma2Rsi {
            source_type,
            smooth_type,
            rsi_period,
            threshold,
            ma,
            fast_period,
            slow_period,
        } => Box::new(Ma2RsiSignal::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            rsi_period,
            threshold,
            ma_deserialize(ma as usize),
            fast_period,
            slow_period,
        )),
        SignalConfig::MaTestingGround {
            source_type,
            ma,
            period,
        } => Box::new(MaTestingGroundSignal::new(
            source_deserialize(source_type as usize),
            ma_deserialize(ma as usize),
            period,
        )),
        SignalConfig::MaSurpass {
            source_type,
            ma,
            period,
        } => Box::new(MaSurpassSignal::new(
            source_deserialize(source_type as usize),
            ma_deserialize(ma as usize),
            period,
        )),
        SignalConfig::MaCross {
            source_type,
            ma,
            period,
        } => Box::new(MaCrossSignal::new(
            source_deserialize(source_type as usize),
            ma_deserialize(ma as usize),
            period,
        )),
        SignalConfig::MaQuadruple {
            source_type,
            ma,
            period,
        } => Box::new(MaQuadrupleSignal::new(
            source_deserialize(source_type as usize),
            ma_deserialize(ma as usize),
            period,
        )),
        SignalConfig::VwapCross {
            source_type,
            period,
        } => Box::new(VwapCrossSignal::new(
            source_deserialize(source_type as usize),
            period,
        )),
        // 2 lines cross
        SignalConfig::Dmi2LinesCross {
            smooth_type,
            adx_period,
            di_period,
        } => Box::new(Dmi2LinesCrossSignal::new(
            smooth_deserialize(smooth_type as usize),
            adx_period,
            di_period,
        )),
        SignalConfig::Vi2LinesCross {
            period,
            smooth_atr,
            period_atr,
        } => Box::new(Vi2LinesCrossSignal::new(
            period,
            smooth_deserialize(smooth_atr as usize),
            period_atr,
        )),
        // Breakout
        SignalConfig::DchMa2Breakout {
            source_type,
            dch_period,
            ma,
            fast_period,
            slow_period,
        } => Box::new(DchMa2BreakoutSignal::new(
            source_deserialize(source_type as usize),
            dch_period,
            ma_deserialize(ma as usize),
            fast_period,
            slow_period,
        )),
    }
}
