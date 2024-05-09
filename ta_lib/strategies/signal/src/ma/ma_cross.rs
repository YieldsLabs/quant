use base::prelude::*;
use core::prelude::*;
use indicator::{ma_indicator, MovingAverageType};
use timeseries::prelude::*;

pub struct MaCrossSignal {
    source_type: SourceType,
    ma: MovingAverageType,
    period: usize,
}

impl MaCrossSignal {
    pub fn new(source_type: SourceType, ma: MovingAverageType, period: f32) -> Self {
        Self {
            source_type,
            ma,
            period: period as usize,
        }
    }
}

impl Signal for MaCrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.source_type, self.period);

        (data.close().cross_over(&ma), data.close().cross_under(&ma))
    }
}
