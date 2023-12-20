use base::{Exit, OHLCVSeries, Price};
use core::prelude::*;
use trend::ast;

pub struct AstExit {
    atr_period: usize,
    multi: f32,
}

impl AstExit {
    pub fn new(atr_period: f32, multi: f32) -> Self {
        Self {
            atr_period: atr_period as usize,
            multi,
        }
    }
}

impl Exit for AstExit {
    fn lookback(&self) -> usize {
        self.atr_period
    }

    fn evaluate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (_, trend) = ast(&data.close, &data.atr(self.atr_period), self.multi);

        (
            data.close.cross_under(&trend),
            data.close.cross_over(&trend),
        )
    }
}
