use base::prelude::*;
use core::prelude::*;
use momentum::dmi;

pub struct DmiReversalSignal {
    smooth_type: Smooth,
    adx_period: usize,
    di_period: usize,
}

impl DmiReversalSignal {
    pub fn new(smooth_type: Smooth, adx_period: f32, di_period: f32) -> Self {
        Self {
            smooth_type,
            adx_period: adx_period as usize,
            di_period: di_period as usize,
        }
    }
}

impl Signal for DmiReversalSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.adx_period, self.di_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (_, di_plus, di_minus) = dmi(
            &data.high,
            &data.low,
            &data.atr(self.di_period, Smooth::SMMA),
            self.smooth_type,
            self.adx_period,
            self.di_period,
        );
        (
            di_plus.cross_over(&di_minus),
            di_plus.cross_under(&di_minus),
        )
    }
}
