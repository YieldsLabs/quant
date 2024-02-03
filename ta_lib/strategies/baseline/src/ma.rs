use base::prelude::*;
use core::prelude::*;
use shared::{ma_indicator, MovingAverageType};

pub struct MABaseLine {
    ma: MovingAverageType,
    period: usize,
}

impl MABaseLine {
    pub fn new(ma: MovingAverageType, period: f32) -> Self {
        Self {
            ma,
            period: period as usize,
        }
    }
}

impl BaseLine for MABaseLine {
    fn lookback(&self) -> usize {
        self.period
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.period);

        (ma.slt(&data.close), ma.sgt(&data.close))
    }
}
