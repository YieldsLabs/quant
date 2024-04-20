use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum SignalConfig {
    // ZeroCross
    AoZeroCross {
        fast_period: f32,
        slow_period: f32,
    },
    ApoZeroCross {
        fast_period: f32,
        slow_period: f32,
    },
    BopZeroCross {
        smooth_type: f32,
        smooth_period: f32,
    },
    CfoZeroCross {
        period: f32,
    },
    CcZeroCross {
        fast_period: f32,
        slow_period: f32,
        smooth_type: f32,
        smooth_period: f32,
    },
    DiZeroCross {
        smooth_type: f32,
        period: f32,
    },
    MacdZeroCross {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    },
    QstickZeroCross {
        smooth_type: f32,
        period: f32,
    },
    RocZeroCross {
        period: f32,
    },
    TrixZeroCross {
        smooth_type: f32,
        period: f32,
    },
    TsiZeroCross {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
    },
    // Signal Line
    DiSignalLine {
        smooth_type: f32,
        period: f32,
        signal_period: f32,
    },
    DsoSignalLine {
        smooth_type: f32,
        smooth_period: f32,
        k_period: f32,
        d_period: f32,
    },
    RsiSignalLine {
        smooth_type: f32,
        rsi_period: f32,
        smooth_signal: f32,
        smooth_period: f32,
        threshold: f32,
    },
    KstSignalLine {
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
    TrixSignalLine {
        smooth_type: f32,
        period: f32,
        signal_period: f32,
    },
    TsiSignalLine {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    },
    QstickSignalLine {
        smooth_type: f32,
        period: f32,
        signal_period: f32,
    },
    StochSignalLine {
        smooth_type: f32,
        period: f32,
        k_period: f32,
        d_period: f32,
    },
    MacdSignalLine {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    },
    // BB
    MacdBb {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
        bb_smooth: f32,
        bb_period: f32,
        factor: f32,
    },
    VwapBb {
        period: f32,
        bb_smooth: f32,
        bb_period: f32,
        factor: f32,
    },
    // Reversal
    DmiReversal {
        smooth_type: f32,
        adx_period: f32,
        di_period: f32,
    },
    SnatrReversal {
        smooth_type: f32,
        atr_period: f32,
        atr_smooth_period: f32,
        threshold: f32,
    },
    ViReversal {
        atr_period: f32,
        period: f32,
    },
    // Flip
    CeFlip {
        period: f32,
        atr_period: f32,
        factor: f32,
    },
    SupFlip {
        atr_period: f32,
        factor: f32,
    },
    // Ma
    MaCross {
        ma: f32,
        period: f32,
    },
    MaSurpass {
        ma: f32,
        period: f32,
    },
    MaQuadruple {
        ma: f32,
        period: f32,
    },
    MaTestingGround {
        ma: f32,
        period: f32,
    },
    Ma2Rsi {
        smooth_type: f32,
        rsi_period: f32,
        threshold: f32,
        ma: f32,
        fast_period: f32,
        slow_period: f32,
    },
    Ma3Cross {
        ma: f32,
        fast_period: f32,
        medium_period: f32,
        slow_period: f32,
    },
    VwapCross {
        period: f32,
    },
    // Pattern
    AoSaucer {
        fast_period: f32,
        slow_period: f32,
    },
    CandlestickTrend {
        candle: f32,
    },
    HighLow {
        period: f32,
    },
    MacdColorSwitch {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    },
    RsiV {
        smooth_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    TiiV {
        smooth_type: f32,
        major_period: f32,
        minor_period: f32,
    },
    // Neutrality
    DsoNeutralityCross {
        smooth_type: f32,
        smooth_period: f32,
        k_period: f32,
        d_period: f32,
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
    TiiNeutralityCross {
        smooth_type: f32,
        major_period: f32,
        minor_period: f32,
    },
    // Breakout
    DchMa2Breakout {
        dch_period: f32,
        ma: f32,
        fast_period: f32,
        slow_period: f32,
    },
}
