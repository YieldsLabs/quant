use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use trend::supertrend;

pub struct SupertrendFlipSignal {
    source: SourceType,
    smooth_atr: Smooth,
    period_atr: usize,
    factor: f32,
}

impl SupertrendFlipSignal {
    pub fn new(source: SourceType, smooth_atr: Smooth, period_atr: f32, factor: f32) -> Self {
        Self {
            source,
            smooth_atr,
            period_atr: period_atr as usize,
            factor,
        }
    }
}

impl Signal for SupertrendFlipSignal {
    fn lookback(&self) -> usize {
        self.period_atr
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (direction, _) = supertrend(
            &data.source(self.source),
            data.close(),
            &data.atr(self.smooth_atr, self.period_atr),
            self.factor,
        );

        (direction.cross_over(&ZERO), direction.cross_under(&ZERO))
    }
}
