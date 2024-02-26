use base::prelude::*;
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
        let (direction, _) = supertrend(
            &data.hl2(),
            &data.close,
            &data.atr(self.atr_period, Smooth::SMMA),
            self.factor,
        );

        let prev_direction = direction.shift(1);

        (
            direction.seq(&1.0) & prev_direction.seq(&-1.0),
            direction.seq(&-1.0) & prev_direction.seq(&1.0),
        )
    }
}
