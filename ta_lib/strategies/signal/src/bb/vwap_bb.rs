use base::prelude::*;
use core::prelude::*;
use volatility::bb;
use volume::vwap;

pub struct VwapBbSignal {
    period: usize,
    bb_smooth: Smooth,
    bb_period: usize,
    factor: f32,
}

impl VwapBbSignal {
    pub fn new(period: f32, bb_smooth: Smooth, bb_period: f32, factor: f32) -> Self {
        Self {
            period: period as usize,
            bb_smooth,
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
        let vwap = vwap(&data.hlc3(), data.volume());

        let (upper_bb, _, lower_bb) = bb(&vwap, self.bb_smooth, self.bb_period, self.factor);

        (vwap.cross_over(&upper_bb), vwap.cross_under(&lower_bb))
    }
}
