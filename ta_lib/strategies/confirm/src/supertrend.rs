use base::prelude::*;
use core::prelude::*;
use trend::supertrend;

const ONE: f32 = 1.0;
const MINUS_ONE: f32 = -1.0;

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
        let (direction, _) = supertrend(
            &data.hl2(),
            &data.close,
            &data.atr(self.atr_period, Smooth::SMMA),
            self.factor,
        );

        let prev_direction = direction.shift(1);
        let back_2_direction = direction.shift(2);

        (
            direction.seq(&ONE) & prev_direction.seq(&ONE) & back_2_direction.seq(&ONE),
            direction.seq(&MINUS_ONE)
                & prev_direction.seq(&MINUS_ONE)
                & back_2_direction.seq(&MINUS_ONE),
        )
    }
}
