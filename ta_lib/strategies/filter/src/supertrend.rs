use base::{Filter, OHLCVSeries, Price};
use core::Series;
use trend::supertrend;

pub struct SupertrendFilter {
    atr_period: usize,
    factor: f32,
}

impl SupertrendFilter {
    pub fn new(atr_period: f32, factor: f32) -> Self {
        Self {
            atr_period: atr_period as usize,
            factor,
        }
    }
}

impl Filter for SupertrendFilter {
    fn lookback(&self) -> usize {
        self.atr_period
    }

    fn apply(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (_, trendline) = supertrend(
            &data.hl2(),
            &data.close,
            &data.atr(self.atr_period),
            self.factor,
        );

        (trendline.gt(&data.close), trendline.lt(&data.close))
    }
}
