use base::prelude::*;
use core::prelude::*;
use momentum::kst;

pub struct KstSignalLineSignal {
    source_type: SourceType,
    smooth_type: Smooth,
    roc_period_first: usize,
    roc_period_second: usize,
    roc_period_third: usize,
    roc_period_fouth: usize,
    period_first: usize,
    period_second: usize,
    period_third: usize,
    period_fouth: usize,
    signal_period: usize,
}

impl KstSignalLineSignal {
    pub fn new(
        source_type: SourceType,
        smooth_type: Smooth,
        roc_period_first: f32,
        roc_period_second: f32,
        roc_period_third: f32,
        roc_period_fouth: f32,
        period_first: f32,
        period_second: f32,
        period_third: f32,
        period_fouth: f32,
        signal_period: f32,
    ) -> Self {
        Self {
            source_type,
            smooth_type,
            roc_period_first: roc_period_first as usize,
            roc_period_second: roc_period_second as usize,
            roc_period_third: roc_period_third as usize,
            roc_period_fouth: roc_period_fouth as usize,
            period_first: period_first as usize,
            period_second: period_second as usize,
            period_third: period_third as usize,
            period_fouth: period_fouth as usize,
            signal_period: signal_period as usize,
        }
    }
}

impl Signal for KstSignalLineSignal {
    fn lookback(&self) -> usize {
        let adjusted_lookback_one = std::cmp::max(self.roc_period_first, self.roc_period_second);
        let adjusted_lookback_two = std::cmp::max(adjusted_lookback_one, self.roc_period_third);
        let adjusted_lookback_three = std::cmp::max(adjusted_lookback_two, self.roc_period_fouth);
        let adjusted_lookback_four = std::cmp::max(adjusted_lookback_three, self.period_first);
        let adjusted_lookback_five = std::cmp::max(adjusted_lookback_four, self.period_second);
        let adjusted_lookback_six = std::cmp::max(adjusted_lookback_five, self.period_third);
        let adjusted_lookback_seven = std::cmp::max(adjusted_lookback_six, self.period_fouth);
        std::cmp::max(adjusted_lookback_seven, self.signal_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let kst = kst(
            &data.source(self.source_type),
            self.smooth_type,
            self.roc_period_first,
            self.roc_period_second,
            self.roc_period_third,
            self.roc_period_fouth,
            self.period_first,
            self.period_second,
            self.period_third,
            self.period_fouth,
        );
        let signal_line = kst.smooth(Smooth::SMA, self.signal_period);

        (kst.cross_over(&signal_line), kst.cross_under(&signal_line))
    }
}
