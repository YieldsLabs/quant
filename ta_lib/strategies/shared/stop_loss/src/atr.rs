use base::{OHLCVSeries, StopLoss};
use core::series::Series;
use volatility::atr::atr;

pub struct ATRStopLoss {
    pub atr_period: usize,
    pub multi: usize,
}

impl StopLoss for ATRStopLoss {
    fn id(&self) -> String {
        format!("ATR_{}_{}", self.atr_period, self.multi)
    }

    fn next(&self, data: &OHLCVSeries) -> (Series<f32>, Series<f32>) {
        let atr = atr(&data.high, &data.low, &data.close, self.atr_period, None);
        let series = Series::from(&data.close);
        let atr_multi = atr * self.multi as f32;

        let long_stop_loss = &series - &atr_multi;
        let short_stop_loss = &series + &atr_multi;

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
            multi: 2,
        };

        assert_eq!(atr_stop_loss.id(), "ATR_14_2");
    }
}
