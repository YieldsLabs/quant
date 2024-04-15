use crate::config::SignalConfig;
use crate::deserialize::{candletrend_deserialize, ma_deserialize, smooth_deserialize};
use base::prelude::*;
use signal::*;

#[inline]
pub fn map_to_signal(config: SignalConfig) -> Box<dyn Signal> {
    match config {
        // Zero Cross
        SignalConfig::AoZeroCross {
            fast_period,
            slow_period,
        } => Box::new(AoZeroCrossSignal::new(fast_period, slow_period)),
        SignalConfig::ApoZeroCross {
            fast_period,
            slow_period,
        } => Box::new(ApoZeroCrossSignal::new(fast_period, slow_period)),
        SignalConfig::BopZeroCross {
            smooth_type,
            smooth_period,
        } => Box::new(BopZeroCrossSignal::new(
            smooth_deserialize(smooth_type as usize),
            smooth_period,
        )),
        SignalConfig::CfoZeroCross { period } => Box::new(CfoZeroCrossSignal::new(period)),
        SignalConfig::CcZeroCross {
            fast_period,
            slow_period,
            smooth_type,
            smooth_period,
        } => Box::new(CcZeroCrossSignal::new(
            fast_period,
            slow_period,
            smooth_deserialize(smooth_type as usize),
            smooth_period,
        )),
        SignalConfig::DiZeroCross {
            smooth_type,
            period,
        } => Box::new(DiZeroCrossSignal::new(
            smooth_deserialize(smooth_type as usize),
            period,
        )),
        SignalConfig::MacdZeroCross {
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(MacdZeroCrossSignal::new(
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
        )),
        SignalConfig::RocZeroCross { period } => Box::new(RocZeroCrossSignal::new(period)),
        SignalConfig::TsiZeroCross {
            smooth_type,
            fast_period,
            slow_period,
        } => Box::new(TsiZeroCrossSignal::new(
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
        )),
        SignalConfig::TrixZeroCross {
            smooth_type,
            period,
        } => Box::new(TrixZeroCrossSignal::new(
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
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(MacdSignalLineSignal::new(
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
        )),
        SignalConfig::RsiSignalLine {
            smooth_type,
            rsi_period,
            smooth_signal,
            smooth_period,
            threshold,
        } => Box::new(RsiSignalLineSignal::new(
            smooth_deserialize(smooth_type as usize),
            rsi_period,
            smooth_deserialize(smooth_signal as usize),
            smooth_period,
            threshold,
        )),
        SignalConfig::DsoSignalLine {
            smooth_type,
            smooth_period,
            k_period,
            d_period,
        } => Box::new(DsoSignalLineSignal::new(
            smooth_deserialize(smooth_type as usize),
            smooth_period,
            k_period,
            d_period,
        )),
        SignalConfig::TrixSignalLine {
            smooth_type,
            period,
            signal_period,
        } => Box::new(TrixSignalLineSignal::new(
            smooth_deserialize(smooth_type as usize),
            period,
            signal_period,
        )),
        SignalConfig::KstSignalLine {
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
            smooth_type,
            period,
            signal_period,
        } => Box::new(DiSignalLineSignal::new(
            smooth_deserialize(smooth_type as usize),
            period,
            signal_period,
        )),
        SignalConfig::TsiSignalLine {
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(TsiSignalLineSignal::new(
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
            period,
            atr_period,
            factor,
        } => Box::new(CeFlipSignal::new(period, atr_period, factor)),
        SignalConfig::SupFlip { atr_period, factor } => {
            Box::new(SupertrendFlipSignal::new(atr_period, factor))
        }
        // Pattern
        SignalConfig::AoSaucer {
            fast_period,
            slow_period,
        } => Box::new(AoSaucerSignal::new(fast_period, slow_period)),
        SignalConfig::MacdColorSwitch {
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
        } => Box::new(MacdColorSwitchSignal::new(
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
        )),
        SignalConfig::TiiV {
            smooth_type,
            major_period,
            minor_period,
        } => Box::new(TiiVSignal::new(
            smooth_deserialize(smooth_type as usize),
            major_period,
            minor_period,
        )),
        SignalConfig::RsiV {
            smooth_type,
            rsi_period,
            threshold,
        } => Box::new(RsiVSignal::new(
            smooth_deserialize(smooth_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::HighLow { period } => Box::new(HighLowSignal::new(period)),
        SignalConfig::CandlestickTrend { candle } => Box::new(CandlestickTrendSignal::new(
            candletrend_deserialize(candle as usize),
        )),
        // BB
        SignalConfig::MacdBb {
            smooth_type,
            fast_period,
            slow_period,
            signal_period,
            bb_period,
            factor,
        } => Box::new(MacdBbSignal::new(
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            signal_period,
            bb_period,
            factor,
        )),
        SignalConfig::VwapBb {
            period,
            smooth_type,
            bb_period,
            factor,
        } => Box::new(VwapBbSignal::new(
            period,
            smooth_deserialize(smooth_type as usize),
            bb_period,
            factor,
        )),
        // Neutrality
        SignalConfig::RsiNeutralityCross {
            smooth_type,
            rsi_period,
            threshold,
        } => Box::new(RsiNeutralityCrossSignal::new(
            smooth_deserialize(smooth_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::RsiNeutralityPullback {
            smooth_type,
            rsi_period,
            threshold,
        } => Box::new(RsiNeutralityPullbackSignal::new(
            smooth_deserialize(smooth_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::RsiNeutralityRejection {
            smooth_type,
            rsi_period,
            threshold,
        } => Box::new(RsiNeutralityRejectionSignal::new(
            smooth_deserialize(smooth_type as usize),
            rsi_period,
            threshold,
        )),
        SignalConfig::DsoNeutralityCross {
            smooth_type,
            smooth_period,
            k_period,
            d_period,
        } => Box::new(DsoNeutralityCrossSignal::new(
            smooth_deserialize(smooth_type as usize),
            smooth_period,
            k_period,
            d_period,
        )),
        // Ma
        SignalConfig::Ma3Cross {
            ma,
            fast_period,
            medium_period,
            slow_period,
        } => Box::new(Ma3CrossSignal::new(
            ma_deserialize(ma as usize),
            fast_period,
            medium_period,
            slow_period,
        )),
        SignalConfig::Ma2Rsi {
            smooth_type,
            rsi_period,
            threshold,
            ma,
            fast_period,
            slow_period,
        } => Box::new(Ma2RsiSignal::new(
            smooth_deserialize(smooth_type as usize),
            rsi_period,
            threshold,
            ma_deserialize(ma as usize),
            fast_period,
            slow_period,
        )),
        SignalConfig::MaTestingGround { ma, period } => Box::new(MaTestingGroundSignal::new(
            ma_deserialize(ma as usize),
            period,
        )),
        SignalConfig::MaSurpass { ma, period } => {
            Box::new(MaSurpassSignal::new(ma_deserialize(ma as usize), period))
        }
        SignalConfig::MaCross { ma, period } => {
            Box::new(MaCrossSignal::new(ma_deserialize(ma as usize), period))
        }
        SignalConfig::MaQuadruple { ma, period } => {
            Box::new(MaQuadrupleSignal::new(ma_deserialize(ma as usize), period))
        }
        SignalConfig::VwapCross { period } => Box::new(VwapCrossSignal::new(period)),
        // Reversal
        SignalConfig::SnatrReversal {
            smooth_type,
            atr_period,
            atr_smooth_period,
            threshold,
        } => Box::new(SnatrReversalSignal::new(
            smooth_deserialize(smooth_type as usize),
            atr_period,
            atr_smooth_period,
            threshold,
        )),
        SignalConfig::DmiReversal {
            smooth_type,
            adx_period,
            di_period,
        } => Box::new(DmiReversalSignal::new(
            smooth_deserialize(smooth_type as usize),
            adx_period,
            di_period,
        )),
        SignalConfig::ViReversal { period, atr_period } => {
            Box::new(ViReversalSignal::new(period, atr_period))
        }
        // Breakout
        SignalConfig::DchMa2Breakout {
            dch_period,
            ma,
            fast_period,
            slow_period,
        } => Box::new(DchMa2BreakoutSignal::new(
            dch_period,
            ma_deserialize(ma as usize),
            fast_period,
            slow_period,
        )),
    }
}
