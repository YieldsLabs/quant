use base::prelude::*;
use core::prelude::*;
use momentum::dmi;
use timeseries::prelude::*;

const ADX_THRESHOLD: f32 = 30.;

pub struct AdxPulse {
    smooth: Smooth,
    period_adx: usize,
    period_di: usize,
    threshold: f32,
}

impl AdxPulse {
    pub fn new(smooth: Smooth, period_adx: f32, period_di: f32, threshold: f32) -> Self {
        Self {
            smooth,
            period_adx: period_adx as usize,
            period_di: period_di as usize,
            threshold,
        }
    }
}

impl Pulse for AdxPulse {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period_adx, self.period_di)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let atr = data.atr(self.smooth, self.period_di);
        let (_, _, adx) = dmi(
            data.high(),
            data.low(),
            &atr,
            self.smooth,
            self.period_adx,
            self.period_di,
        );

        let barrier = ADX_THRESHOLD - self.threshold;

        (adx.sgt(&barrier), adx.sgt(&barrier))
    }
}
