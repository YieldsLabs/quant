use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use volume::nvol;

const NVOL_LINE: f32 = 100.0;

pub struct NvolPulse {
    smooth: Smooth,
    period: usize,
}

impl NvolPulse {
    pub fn new(smooth: Smooth, period: f32) -> Self {
        Self {
            smooth,
            period: period as usize,
        }
    }
}

impl Pulse for NvolPulse {
    fn lookback(&self) -> usize {
        self.period
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let nvol = nvol(data.volume(), self.smooth, self.period);

        (nvol.sgt(&NVOL_LINE), nvol.sgt(&NVOL_LINE))
    }
}
