use base::prelude::*;
use core::prelude::*;
use momentum::tdfi;

const TDFI_UPPER_LINE: f32 = 0.05;
const TDFI_LOWER_LINE: f32 = -0.05;

pub struct TdfiPulse {
    source_type: SourceType,
    smooth_type: Smooth,
    period: usize,
    n: usize,
}

impl TdfiPulse {
    pub fn new(source_type: SourceType, smooth_type: Smooth, period: f32, n: f32) -> Self {
        Self {
            source_type,
            smooth_type,
            period: period as usize,
            n: n as usize,
        }
    }
}

impl Pulse for TdfiPulse {
    fn lookback(&self) -> usize {
        self.period
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tdfi = tdfi(
            &data.source(self.source_type),
            self.smooth_type,
            self.period,
            self.n,
        );

        (tdfi.sgt(&TDFI_UPPER_LINE), tdfi.slt(&TDFI_LOWER_LINE))
    }
}
