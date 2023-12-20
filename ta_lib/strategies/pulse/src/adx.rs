use base::{OHLCVSeries, Price, Pulse};
use core::prelude::*;
use momentum::dmi;

const ADX_TREND: f32 = 25.0;

pub struct ADXPulse {
    adx_period: usize,
    di_period: usize,
    threshold: f32,
}

impl ADXPulse {
    pub fn new(adx_period: f32, di_period: f32, threshold: f32) -> Self {
        Self {
            adx_period: adx_period as usize,
            di_period: di_period as usize,
            threshold,
        }
    }
}

impl Pulse for ADXPulse {
    fn lookback(&self) -> usize {
        std::cmp::max(self.adx_period, self.di_period)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (adx, _, _) = dmi(
            &data.high,
            &data.low,
            &data.atr(self.di_period),
            self.adx_period,
            self.di_period,
        );
        let upper_adx_trend = ADX_TREND + self.threshold;

        (
            adx.sgt(&upper_adx_trend) & adx.sgt(&adx.shift(1)),
            adx.sgt(&upper_adx_trend) & adx.sgt(&adx.shift(1)),
        )
    }
}
