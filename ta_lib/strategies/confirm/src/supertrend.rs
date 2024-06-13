use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use trend::supertrend;

pub struct SupertrendConfirm {
    source_type: SourceType,
    atr_period: usize,
    factor: f32,
}

impl SupertrendConfirm {
    pub fn new(source_type: SourceType, atr_period: f32, factor: f32) -> Self {
        Self {
            source_type,
            atr_period: atr_period as usize,
            factor,
        }
    }
}

impl Confirm for SupertrendConfirm {
    fn lookback(&self) -> usize {
        self.atr_period
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (direction, _) = supertrend(
            &data.source(self.source_type),
            data.close(),
            &data.atr(self.atr_period),
            self.factor,
        );

        (direction.sgt(&ZERO), direction.slt(&ZERO))
    }
}
