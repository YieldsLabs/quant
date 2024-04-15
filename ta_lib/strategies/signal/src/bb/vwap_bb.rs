use base::prelude::*;
use core::prelude::*;
use volatility::bb;
use volume::vwap;

pub struct VwapBbSignal {
    period: usize,
    smooth_type: Smooth,
    bb_period: usize,
    factor: f32,
}

impl VwapBbSignal {
    pub fn new(period: f32, smooth_type: Smooth, bb_period: f32, factor: f32) -> Self {
        Self {
            period: period as usize,
            smooth_type,
            bb_period: bb_period as usize,
            factor,
        }
    }
}

impl Signal for VwapBbSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.bb_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let vwap = vwap(&data.hlc3(), &data.volume);
        let (upper_bb, _, lower_bb) = bb(&vwap, self.smooth_type, self.bb_period, self.factor);

        (vwap.cross_over(&upper_bb), vwap.cross_under(&lower_bb))
    }
}
