use base::{OHLCVSeries, StopLoss};
use core::Series;
use volatility::atr;

pub struct ATRStopLoss {
    pub period: usize,
    pub multi: f32,
}

impl ATRStopLoss {
    pub fn new(period: f32, multi: f32) -> Self {
        Self {
            period: period as usize,
            multi,
        }
    }
}

impl StopLoss for ATRStopLoss {
    fn lookback(&self) -> usize {
        self.period
    }

    fn next(&self, data: &OHLCVSeries) -> (Series<f32>, Series<f32>) {
        let atr = atr(&data.high, &data.low, &data.close, self.period, None);

        let high = Series::from(&data.high);
        let low = Series::from(&data.low);

        let atr_multi = atr * self.multi;

        let long_stop_loss = low - &atr_multi;
        let short_stop_loss = high + &atr_multi;

        (long_stop_loss, short_stop_loss)
    }
}
