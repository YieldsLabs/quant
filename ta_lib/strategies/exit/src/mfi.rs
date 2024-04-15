use base::prelude::*;
use core::prelude::*;
use volume::mfi;

const MFI_OVERBOUGHT: f32 = 80.0;
const MFI_OVERSOLD: f32 = 20.0;

pub struct MfiExit {
    period: usize,
    threshold: f32,
}

impl MfiExit {
    pub fn new(period: f32, threshold: f32) -> Self {
        Self {
            period: period as usize,
            threshold,
        }
    }
}

impl Exit for MfiExit {
    fn lookback(&self) -> usize {
        self.period
    }

    fn evaluate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let mfi = mfi(&data.hlc3(), &data.volume, self.period);
        let upper_bound = MFI_OVERBOUGHT - self.threshold;
        let lower_bound = MFI_OVERSOLD + self.threshold;

        (mfi.cross_under(&upper_bound), mfi.cross_over(&lower_bound))
    }
}
