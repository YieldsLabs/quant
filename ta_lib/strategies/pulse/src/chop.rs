use base::prelude::*;
use core::prelude::*;
use trend::chop;

const CHOP_MIDDLE_LINE: f32 = 38.2;

pub struct CHOPPulse {
    period: usize,
    atr_period: usize,
    threshold: f32,
}

impl CHOPPulse {
    pub fn new(period: f32, atr_period: f32, threshold: f32) -> Self {
        Self {
            period: period as usize,
            atr_period: atr_period as usize,
            threshold,
        }
    }
}

impl Pulse for CHOPPulse {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.atr_period)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let chop = chop(
            &data.high,
            &data.low,
            &data.atr(self.atr_period),
            self.period,
        );
        let lower_chop = CHOP_MIDDLE_LINE + self.threshold;

        (chop.slt(&lower_chop), chop.slt(&lower_chop))
    }
}
