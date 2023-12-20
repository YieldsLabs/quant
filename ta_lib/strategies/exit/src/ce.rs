use base::{Exit, OHLCVSeries, Price};
use core::prelude::*;
use trend::ce;

const CE_MIDDLE: f32 = 0.0;

pub struct CeExit {
    period: usize,
    atr_period: usize,
    multi: f32,
}

impl CeExit {
    pub fn new(period: f32, atr_period: f32, multi: f32) -> Self {
        Self {
            period: period as usize,
            atr_period: atr_period as usize,
            multi,
        }
    }
}

impl Exit for CeExit {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.atr_period)
    }

    fn evaluate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (direction, trend) = ce(
            &data.high,
            &data.low,
            &data.close,
            &data.atr(self.atr_period),
            self.period,
            self.multi,
        );

        (
            data.close.cross_under(&trend) & direction.slt(&CE_MIDDLE),
            data.close.cross_over(&trend) & direction.sgt(&CE_MIDDLE),
        )
    }
}
