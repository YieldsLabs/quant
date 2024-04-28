use base::prelude::*;
use core::prelude::*;
use momentum::dmi;

const ADX_LOWER_BARRIER: f32 = 25.;

pub struct AdxPulse {
    smooth_type: Smooth,
    adx_period: usize,
    di_period: usize,
    threshold: f32,
}

impl AdxPulse {
    pub fn new(smooth_type: Smooth, adx_period: f32, di_period: f32, threshold: f32) -> Self {
        Self {
            smooth_type,
            adx_period: adx_period as usize,
            di_period: di_period as usize,
            threshold,
        }
    }
}

impl Pulse for AdxPulse {
    fn lookback(&self) -> usize {
        std::cmp::max(self.adx_period, self.di_period)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (adx, _, _) = dmi(
            data.high(),
            data.low(),
            &data.atr(self.di_period, Smooth::SMMA),
            self.smooth_type,
            self.adx_period,
            self.di_period,
        );
        let adx_lower = ADX_LOWER_BARRIER + self.threshold;

        (adx.sgt(&adx_lower), adx.sgt(&adx_lower))
    }
}
