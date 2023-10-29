use base::{OHLCVSeries, Signal};
use core::Series;
use shared::{rsi_indicator, RSIType};

const RSI_NEUTRALITY: f32 = 50.0;

pub struct RSIMaPullbackSignal {
    rsi_type: RSIType,
    rsi_period: usize,
    smoothing_period: usize,
    threshold: f32,
}

impl RSIMaPullbackSignal {
    pub fn new(rsi_type: RSIType, rsi_period: f32, smoothing_period: f32, threshold: f32) -> Self {
        Self {
            rsi_type,
            rsi_period: rsi_period as usize,
            smoothing_period: smoothing_period as usize,
            threshold,
        }
    }
}

impl Signal for RSIMaPullbackSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.rsi_period, self.smoothing_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi_indicator(&self.rsi_type, data, self.rsi_period);
        let rsi_ma = rsi.ma(self.smoothing_period);

        let long = rsi.gt(&rsi_ma)
            & rsi.slt(RSI_NEUTRALITY + self.threshold)
            & rsi.shift(1).eq(&rsi_ma.shift(1))
            & rsi.shift(2).gt(&rsi.shift(1))
            & rsi.shift(3).lt(&rsi_ma.shift(3));

        let short = rsi.lt(&rsi_ma)
            & rsi.sgt(RSI_NEUTRALITY - self.threshold)
            & rsi.shift(1).eq(&rsi_ma.shift(1))
            & rsi.shift(2).lt(&rsi.shift(1))
            & rsi.shift(3).gt(&rsi_ma.shift(3));

        (long, short)
    }
}
