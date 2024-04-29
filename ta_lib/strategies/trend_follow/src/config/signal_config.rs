use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum SignalConfig {
    // ZeroCross
    AoZeroCross {
        source_type: f32,
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
    },
    BopZeroCross {
        smooth_type: f32,
        smooth_period: f32,
    },
    CfoZeroCross {
        source_type: f32,
        period: f32,
    },
    CcZeroCross {
        source_type: f32,
        fast_period: f32,
        slow_period: f32,
        smooth_type: f32,
        smooth_period: f32,
    },
    DiZeroCross {
        source_type: f32,
        smooth_type: f32,
        period: f32,
    },
    MacdZeroCross {
        source_type: f32,
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
        source_type: f32,
        period: f32,
    },
    TrixZeroCross {
        source_type: f32,
        smooth_type: f32,
        period: f32,
    },
    TsiZeroCross {
        source_type: f32,
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
    },
    // Signal Line
    DiSignalLine {
        source_type: f32,
        smooth_type: f32,
        period: f32,
        signal_period: f32,
    },
    DsoSignalLine {
        source_type: f32,
        smooth_type: f32,
        smooth_period: f32,
        k_period: f32,
        d_period: f32,
    },
    RsiSignalLine {
        source_type: f32,
        smooth_type: f32,
        rsi_period: f32,
        smooth_signal: f32,
        smooth_period: f32,
        threshold: f32,
    },
    KstSignalLine {
        source_type: f32,
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
        source_type: f32,
        smooth_type: f32,
        period: f32,
        signal_period: f32,
    },
    TsiSignalLine {
        source_type: f32,
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
        source_type: f32,
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    },
    // BB
    MacdBb {
        source_type: f32,
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
        bb_smooth: f32,
        bb_period: f32,
        factor: f32,
    },
    VwapBb {
        source_type: f32,
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
        source_type: f32,
        atr_period: f32,
        factor: f32,
    },
    // Ma
    MaCross {
        source_type: f32,
        ma: f32,
        period: f32,
    },
    MaSurpass {
        source_type: f32,
        ma: f32,
        period: f32,
    },
    MaQuadruple {
        source_type: f32,
        ma: f32,
        period: f32,
    },
    MaTestingGround {
        source_type: f32,
        ma: f32,
        period: f32,
    },
    Ma2Rsi {
        source_type: f32,
        smooth_type: f32,
        rsi_period: f32,
        threshold: f32,
        ma: f32,
        fast_period: f32,
        slow_period: f32,
    },
    Ma3Cross {
        source_type: f32,
        ma: f32,
        fast_period: f32,
        medium_period: f32,
        slow_period: f32,
    },
    VwapCross {
        source_type: f32,
        period: f32,
    },
    // Pattern
    AoSaucer {
        source_type: f32,
        smooth_type: f32,
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
        source_type: f32,
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    },
    RsiV {
        source_type: f32,
        smooth_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    TiiV {
        source_type: f32,
        smooth_type: f32,
        major_period: f32,
        minor_period: f32,
    },
    // Neutrality
    DsoNeutralityCross {
        source_type: f32,
        smooth_type: f32,
        smooth_period: f32,
        k_period: f32,
        d_period: f32,
    },
    RsiNeutralityCross {
        source_type: f32,
        smooth_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    RsiNeutralityPullback {
        source_type: f32,
        smooth_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    RsiNeutralityRejection {
        source_type: f32,
        smooth_type: f32,
        rsi_period: f32,
        threshold: f32,
    },
    TiiNeutralityCross {
        source_type: f32,
        smooth_type: f32,
        major_period: f32,
        minor_period: f32,
    },
    // Breakout
    DchMa2Breakout {
        source_type: f32,
        dch_period: f32,
        ma: f32,
        fast_period: f32,
        slow_period: f32,
    },
}
