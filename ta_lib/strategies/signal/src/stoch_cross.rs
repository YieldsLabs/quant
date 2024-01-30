use base::prelude::*;
use core::prelude::*;
use momentum::stochosc;

const LOWER_LINE: f32 = 20.0;
const UPPER_LINE: f32 = 80.0;

pub struct StochCrossSignal {
    period: usize,
    k_period: usize,
    d_period: usize,
}

impl StochCrossSignal {
    pub fn new(period: f32, k_period: f32, d_period: f32) -> Self {
        Self {
            period: period as usize,
            k_period: k_period as usize,
            d_period: d_period as usize,
        }
    }
}

impl Signal for StochCrossSignal {
    fn lookback(&self) -> usize {
        let adjusted_lookback = std::cmp::max(self.period, self.k_period);
        std::cmp::max(adjusted_lookback, self.d_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (k, d) = stochosc(
            &data.high,
            &data.low,
            &data.close,
            self.period,
            self.k_period,
            self.d_period,
        );

        (
            k.cross_over(&d) & d.slt(&LOWER_LINE),
            k.cross_under(&d) & d.sgt(&UPPER_LINE),
        )
    }
}
