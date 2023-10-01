use base::{OHLCVSeries, Signal};
use core::Series;
use shared::{rsi_indicator, RSIType};

pub struct RSIVSignal {
    rsi_type: RSIType,
    rsi_period: usize,
    lower_barrier: f32,
    upper_barrier: f32,
}

impl RSIVSignal {
    pub fn new(rsi_type: RSIType, rsi_period: f32, lower_barrier: f32, upper_barrier: f32) -> Self {
        Self {
            rsi_type,
            rsi_period: rsi_period as usize,
            lower_barrier,
            upper_barrier,
        }
    }
}

impl Signal for RSIVSignal {
    fn lookback(&self) -> usize {
        self.rsi_period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi_indicator(&self.rsi_type, data, self.rsi_period);

        let long_signal = rsi.sgt(self.lower_barrier)
            & rsi.shift(1).slt(self.upper_barrier)
            & rsi.shift(2).sgt(self.lower_barrier);
        let short_signal = rsi.slt(self.upper_barrier)
            & rsi.shift(1).sgt(self.upper_barrier)
            & rsi.shift(2).slt(self.upper_barrier);

        (long_signal, short_signal)
    }
}
