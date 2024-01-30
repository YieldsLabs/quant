use base::prelude::*;
use core::prelude::*;
use momentum::rsi;

const RSI_OVERBOUGHT: f32 = 70.0;
const RSI_OVERSOLD: f32 = 30.0;

pub struct RSIExit {
    period: usize,
    threshold: f32,
}

impl RSIExit {
    pub fn new(period: f32, threshold: f32) -> Self {
        Self {
            period: period as usize,
            threshold,
        }
    }
}

impl Exit for RSIExit {
    fn lookback(&self) -> usize {
        self.period
    }

    fn evaluate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.close, self.period);
        let upper_bound = RSI_OVERBOUGHT + self.threshold;
        let lower_bound = RSI_OVERSOLD - self.threshold;

        (rsi.cross_over(&upper_bound), rsi.cross_under(&lower_bound))
    }
}
