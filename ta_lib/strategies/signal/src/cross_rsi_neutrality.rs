use base::{OHLCVSeries, Signal};
use core::Series;
use shared::{rsi_indicator, RSIType};

pub struct CrossRSINeutralitySignal {
    rsi_type: RSIType,
    rsi_period: usize,
    threshold: f32,
}

impl CrossRSINeutralitySignal {
    pub fn new(rsi_type: RSIType, rsi_period: f32, threshold: f32) -> Self {
        Self {
            rsi_type,
            rsi_period: rsi_period as usize,
            threshold,
        }
    }
}

impl Signal for CrossRSINeutralitySignal {
    fn lookback(&self) -> usize {
        self.rsi_period
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi_indicator(&self.rsi_type, data, self.rsi_period);

        let long_signal = rsi.sgt(50.0 + self.threshold)
            & rsi.shift(1).sgt(50.0)
            & rsi.shift(2).slt(50.0)
            & rsi.shift(3).slt(50.0)
            & rsi.shift(4).slt(50.0);

        let short_signal = rsi.slt(50.0 - self.threshold)
            & rsi.shift(1).slt(50.0)
            & rsi.shift(2).sgt(50.0)
            & rsi.shift(3).sgt(50.0)
            & rsi.shift(4).sgt(50.0);

        (long_signal, short_signal)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
