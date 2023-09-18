use base::{OHLCVSeries, StopLoss};
use core::series::Series;
use volatility::atr;

pub struct ATRStopLoss {
    pub atr_period: usize,
    pub multi: f32,
}

impl StopLoss for ATRStopLoss {
    fn id(&self) -> String {
        format!("ATR_{}:{:.1}", self.atr_period, self.multi)
    }

    fn next(&self, data: &OHLCVSeries) -> (Series<f32>, Series<f32>) {
        let atr = atr(&data.high, &data.low, &data.close, self.atr_period, None);

        let high = Series::from(&data.high);
        let low = Series::from(&data.low);

        let atr_multi = atr * self.multi;

        let long_stop_loss = low - &atr_multi;
        let short_stop_loss = high + &atr_multi;

        (long_stop_loss, short_stop_loss)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_atr_stop_loss_id() {
        let atr_stop_loss = ATRStopLoss {
            atr_period: 14,
            multi: 2.0,
        };

        assert_eq!(atr_stop_loss.id(), "ATR_14:2.0");
    }
}
