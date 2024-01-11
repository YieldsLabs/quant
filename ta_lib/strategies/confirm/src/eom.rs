use base::prelude::*;
use core::prelude::*;
use volume::eom;

const EOM_FILTER: f32 = 0.0;

pub struct EOMConfirm {
    period: usize,
    divisor: f32,
}

impl EOMConfirm {
    pub fn new(period: f32, divisor: f32) -> Self {
        Self {
            period: period as usize,
            divisor,
        }
    }
}

impl Confirm for EOMConfirm {
    fn lookback(&self) -> usize {
        self.period
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let eom = eom(
            &data.hl2(),
            &data.high,
            &data.low,
            &data.volume,
            self.period,
            self.divisor,
        );

        (eom.sgt(&EOM_FILTER), eom.slt(&EOM_FILTER))
    }
}
