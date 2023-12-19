use base::{OHLCVSeries, Signal};
use core::{Comparator, Series};
use shared::{rsi_indicator, RSIType};

const RSI_NEUTRALITY: f32 = 50.0;

pub struct RSINeutralityPullbackSignal {
    rsi_type: RSIType,
    rsi_period: usize,
    threshold: f32,
}

impl RSINeutralityPullbackSignal {
    pub fn new(rsi_type: RSIType, rsi_period: f32, threshold: f32) -> Self {
        Self {
            rsi_type,
            rsi_period: rsi_period as usize,
            threshold,
        }
    }
}

impl Signal for RSINeutralityPullbackSignal {
    fn lookback(&self) -> usize {
        self.rsi_period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi_indicator(&self.rsi_type, data, self.rsi_period);

        let long = rsi.shift(1).sgt(&RSI_NEUTRALITY)
            & rsi.shift(1).slt(&(RSI_NEUTRALITY + self.threshold))
            & rsi.shift(1).slt(&rsi.shift(2))
            & rsi.shift(2).sgt(&RSI_NEUTRALITY)
            & rsi.shift(3).slt(&RSI_NEUTRALITY);

        let short = rsi.shift(1).slt(&RSI_NEUTRALITY)
            & rsi.shift(1).sgt(&(RSI_NEUTRALITY - self.threshold))
            & rsi.shift(1).sgt(&rsi.shift(2))
            & rsi.shift(2).slt(&RSI_NEUTRALITY)
            & rsi.shift(3).sgt(&RSI_NEUTRALITY);

        (long, short)
    }
}
