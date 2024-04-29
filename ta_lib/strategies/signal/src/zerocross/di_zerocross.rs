use base::prelude::*;
use core::prelude::*;
use momentum::di;

pub struct DiZeroCrossSignal {
    source_type: SourceType,
    smooth_type: Smooth,
    period: usize,
}

impl DiZeroCrossSignal {
    pub fn new(source_type: SourceType, smooth_type: Smooth, period: f32) -> Self {
        Self {
            source_type,
            smooth_type,
            period: period as usize,
        }
    }
}

impl Signal for DiZeroCrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let di = di(
            &data.source(self.source_type),
            self.smooth_type,
            self.period,
        );

        (di.cross_over(&ZERO_LINE), di.cross_under(&ZERO_LINE))
    }
}
