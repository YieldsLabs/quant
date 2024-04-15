use base::prelude::*;
use core::prelude::*;
use volume::vwap;

pub struct VwapCrossSignal {
    period: usize,
}

impl VwapCrossSignal {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Signal for VwapCrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let vwap = vwap(&data.hlc3(), &data.volume);

        (data.close.cross_over(&vwap), data.close.cross_under(&vwap))
    }
}
