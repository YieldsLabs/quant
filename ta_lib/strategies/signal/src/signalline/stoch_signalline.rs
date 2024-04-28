use base::prelude::*;
use core::prelude::*;
use momentum::stochosc;

pub struct StochSignalLineSignal {
    smooth_type: Smooth,
    period: usize,
    k_period: usize,
    d_period: usize,
}

impl StochSignalLineSignal {
    pub fn new(smooth_type: Smooth, period: f32, k_period: f32, d_period: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
            k_period: k_period as usize,
            d_period: d_period as usize,
        }
    }
}

impl Signal for StochSignalLineSignal {
    fn lookback(&self) -> usize {
        let adjusted_lookback = std::cmp::max(self.period, self.k_period);
        std::cmp::max(adjusted_lookback, self.d_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (k, d) = stochosc(
            data.high(),
            data.low(),
            data.close(),
            self.smooth_type,
            self.period,
            self.k_period,
            self.d_period,
        );

        (k.cross_over(&d), k.cross_under(&d))
    }
}
