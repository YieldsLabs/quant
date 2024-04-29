use base::prelude::*;
use core::prelude::*;
use volume::vwap;

pub struct VwapCrossSignal {
    source_type: SourceType,
    period: usize,
}

impl VwapCrossSignal {
    pub fn new(source_type: SourceType, period: f32) -> Self {
        Self {
            source_type,
            period: period as usize,
        }
    }
}

impl Signal for VwapCrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let vwap = vwap(&data.source(self.source_type), data.volume());

        (
            data.close().cross_over(&vwap),
            data.close().cross_under(&vwap),
        )
    }
}
