use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use volume::nvol;

const NVOL_LINE: f32 = 100.0;

pub struct NvolPulse {
    smooth_type: Smooth,
    period: usize,
}

impl NvolPulse {
    pub fn new(smooth_type: Smooth, period: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
        }
    }
}

impl Pulse for NvolPulse {
    fn lookback(&self) -> usize {
        self.period
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let nvol = nvol(data.volume(), self.smooth_type, self.period);

        (nvol.sgt(&NVOL_LINE), nvol.sgt(&NVOL_LINE))
    }
}
