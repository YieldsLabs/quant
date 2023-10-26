use base::{OHLCVSeries, Price, Signal};
use core::Series;
use volatility::snatr;

const SNATR_UPPER_BARRIER: f32 = 0.8;
const SNATR_LOWER_BARRIER: f32 = 0.2;

pub struct SNATRSignal {
    atr_period: usize,
    atr_smoothing_period: usize,
    threshold: f32,
}

impl SNATRSignal {
    pub fn new(atr_period: f32, atr_smoothing_period: f32, threshold: f32) -> Self {
        Self {
            atr_period: atr_period as usize,
            atr_smoothing_period: atr_smoothing_period as usize,
            threshold,
        }
    }
}

impl Signal for SNATRSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.atr_period, self.atr_smoothing_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let snatr = snatr(
            &data.atr(self.atr_period),
            self.atr_period,
            self.atr_smoothing_period,
        );

        (
            snatr.cross_under_line(SNATR_UPPER_BARRIER - self.threshold),
            snatr.cross_over_line(SNATR_LOWER_BARRIER + self.threshold),
        )
    }
}
