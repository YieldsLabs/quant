use base::prelude::*;
use core::prelude::*;
use momentum::dmi;
use timeseries::prelude::*;

const ADX_LOWER_BARRIER: f32 = 25.;

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
        let (_, _, adx) = dmi(
            data.high(),
            data.low(),
            &data.atr(self.smooth, self.period_di),
            self.smooth,
            self.period_adx,
            self.period_di,
        );
        let prev_adx = adx.shift(1);

        let adx_lower = ADX_LOWER_BARRIER + self.threshold;

        (
            adx.sgt(&adx_lower) & adx.sgt(&prev_adx),
            adx.sgt(&adx_lower) & adx.sgt(&prev_adx),
        )
    }
}
