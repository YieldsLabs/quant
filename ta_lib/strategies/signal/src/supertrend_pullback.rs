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

        let above = data.close.gt(&trendline);
        let below = data.close.lt(&trendline);

        (
            data.low.lte(&trendline)
                & data.close.gt(&trendline)
                & below.shift(1)
                & below.shift(2)
                & direction.seq(1.0),
            data.high.gte(&trendline)
                & data.close.lt(&trendline)
                & above.shift(1)
                & above.shift(2)
                & direction.seq(-1.0),
        )
    }
}
