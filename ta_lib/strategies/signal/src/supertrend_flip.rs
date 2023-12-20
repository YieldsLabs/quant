use base::{OHLCVSeries, Price, Signal};
use core::prelude::*;
use trend::supertrend;

pub struct SupertrendFlipSignal {
    atr_period: usize,
    factor: f32,
}

impl SupertrendFlipSignal {
    pub fn new(atr_period: f32, factor: f32) -> Self {
        Self {
            atr_period: atr_period as usize,
            factor,
        }
    }
}

impl Signal for SupertrendFlipSignal {
    fn lookback(&self) -> usize {
        self.atr_period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (_, trendline) = supertrend(
            &data.hl2(),
            &data.close,
            &data.atr(self.atr_period),
            self.factor,
        );

        (
            trendline.cross_under(&data.close),
            trendline.cross_over(&data.close),
        )
    }
}
