use base::{Exit, OHLCVSeries, Price};
use core::Series;

pub struct ChExit {
    period: usize,
    atr_period: usize,
    multi: f32,
}

impl ChExit {
    pub fn new(period: f32, atr_period: f32, multi: f32) -> Self {
        Self {
            period: period as usize,
            atr_period: atr_period as usize,
            multi,
        }
    }
}

impl Exit for ChExit {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.atr_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let atr = data.atr(self.period);
        let atr_multi = atr * self.multi;

        let ch_long = data.high.highest(self.period) - &atr_multi;
        let ch_short = data.low.lowest(self.period) + &atr_multi;

        (
            data.close.cross_under(&ch_long),
            data.close.cross_over(&ch_short),
        )
    }
}
