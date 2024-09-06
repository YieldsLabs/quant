use base::prelude::*;
use core::prelude::*;
use indicator::{ma_indicator, MovingAverageType};
use timeseries::prelude::*;

pub struct MaExit {
    source_type: SourceType,
    ma: MovingAverageType,
    period: usize,
}

impl MaExit {
    pub fn new(source_type: SourceType, ma: MovingAverageType, period: f32) -> Self {
        Self {
            source_type,
            ma,
            period: period as usize,
        }
    }
}

impl Exit for MaExit {
    fn lookback(&self) -> usize {
        self.period
    }

    fn close(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.source_type, self.period);

        (data.close().cross_under(&ma), data.close().cross_over(&ma))
    }
}
