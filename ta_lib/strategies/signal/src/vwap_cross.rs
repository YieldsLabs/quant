use base::{OHLCVSeries, Price, Signal};
use core::{Cross, Series};
use volume::vwap;

pub struct VWAPCrossSignal {
    period: usize,
}

impl VWAPCrossSignal {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Signal for VWAPCrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let vwap = vwap(&data.hlc3(), &data.volume);

        (data.close.cross_over(&vwap), data.close.cross_under(&vwap))
    }
}
