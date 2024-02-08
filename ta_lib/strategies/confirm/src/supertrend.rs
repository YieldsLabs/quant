use base::prelude::*;
use core::prelude::*;
use trend::supertrend;

pub struct SupertrendConfirm {
    atr_period: usize,
    factor: f32,
}

impl SupertrendConfirm {
    pub fn new(atr_period: f32, factor: f32) -> Self {
        Self {
            atr_period: atr_period as usize,
            factor,
        }
    }
}

impl Confirm for SupertrendConfirm {
    fn lookback(&self) -> usize {
        self.atr_period
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (_, trendline) = supertrend(
            &data.hl2(),
            &data.close,
            &data.atr(self.atr_period),
            self.factor,
        );

        (data.close.sgt(&trendline), data.close.slt(&trendline))
    }
}
