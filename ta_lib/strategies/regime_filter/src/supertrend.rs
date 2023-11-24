use base::{OHLCVSeries, Price, Regime};
use core::Series;
use trend::supertrend;

const SUP_ZERO: f32 = 0.0;

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

impl Regime for SupertrendFilter {
    fn lookback(&self) -> usize {
        self.atr_period
    }

    fn apply(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (direction, trendline) = supertrend(
            &data.hl2(),
            &data.close,
            &data.atr(self.atr_period),
            self.factor,
        );

        (
            data.close.gt(&trendline) & direction.sgt(SUP_ZERO),
            data.close.lt(&trendline) & direction.slt(SUP_ZERO),
        )
    }
}
