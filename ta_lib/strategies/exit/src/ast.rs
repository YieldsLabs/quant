use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use trend::ast;

pub struct AstExit {
    source_type: SourceType,
    atr_period: usize,
    factor: f32,
}

impl AstExit {
    pub fn new(source_type: SourceType, atr_period: f32, factor: f32) -> Self {
        Self {
            source_type,
            atr_period: atr_period as usize,
            factor,
        }
    }
}

impl Exit for AstExit {
    fn lookback(&self) -> usize {
        self.atr_period
    }

    fn close(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (direction, _) = ast(
            &data.source(self.source_type),
            &data.atr(Smooth::SMMA, self.atr_period),
            self.factor,
        );

        (direction.cross_over(&ZERO), direction.cross_under(&ZERO))
    }
}
