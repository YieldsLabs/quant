use base::{OHLCVSeries, Price, Signal};
use core::Series;
use trend::supertrend;

pub struct SupertrendPullBackSignal {
    atr_period: usize,
    factor: f32,
}

impl SupertrendPullBackSignal {
    pub fn new(atr_period: f32, factor: f32) -> Self {
        Self {
            atr_period: atr_period as usize,
            factor,
        }
    }
}

impl Signal for SupertrendPullBackSignal {
    fn lookback(&self) -> usize {
        self.atr_period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (direction, trendline) = supertrend(
            &data.hl2(),
            &data.close,
            &data.atr(self.atr_period),
            self.factor,
        );

        (
            direction.shift(1).seq(1.0) & trendline.gt(&data.low) & trendline.lt(&data.close),
            direction.shift(1).seq(-1.0) & trendline.lt(&data.high) & trendline.gt(&data.close),
        )
    }
}
