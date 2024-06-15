use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use trend::ast;

pub struct AstExit {
    source_type: SourceType,
    smooth_atr: Smooth,
    period_atr: usize,
    factor: f32,
}

impl AstExit {
    pub fn new(source_type: SourceType, smooth_atr: Smooth, period_atr: f32, factor: f32) -> Self {
        Self {
            source_type,
            smooth_atr,
            period_atr: period_atr as usize,
            factor,
        }
    }
}

impl Exit for AstExit {
    fn lookback(&self) -> usize {
        self.period_atr
    }

    fn close(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (direction, _) = ast(
            &data.source(self.source_type),
            &data.atr(self.smooth_atr, self.period_atr),
            self.factor,
        );

        (direction.cross_over(&ZERO), direction.cross_under(&ZERO))
    }
}
