use base::prelude::*;
use core::prelude::*;
use shared::{ma_indicator, MovingAverageType};

pub struct MACrossSignal {
    ma: MovingAverageType,
    period: usize,
}

impl MACrossSignal {
    pub fn new(ma: MovingAverageType, period: f32) -> Self {
        Self {
            ma,
            period: period as usize,
        }
    }
}

impl Signal for MACrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.period);

        (data.close.cross_over(&ma), data.close.cross_under(&ma))
    }
}
