use base::prelude::*;
use core::prelude::*;
use momentum::dso;

pub struct DsoSignalLineSignal {
    smooth_type: Smooth,
    smooth_period: usize,
    k_period: usize,
    d_period: usize,
}

impl DsoSignalLineSignal {
    pub fn new(smooth_type: Smooth, smooth_period: f32, k_period: f32, d_period: f32) -> Self {
        Self {
            smooth_type,
            smooth_period: smooth_period as usize,
            k_period: k_period as usize,
            d_period: d_period as usize,
        }
    }
}

impl Signal for DsoSignalLineSignal {
    fn lookback(&self) -> usize {
        let period = std::cmp::max(self.smooth_period, self.k_period);
        std::cmp::max(period, self.d_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (k, d) = dso(
            &data.close(),
            self.smooth_type,
            self.smooth_period,
            self.k_period,
            self.d_period,
        );

        (k.cross_over(&d), k.cross_under(&d))
    }
}
