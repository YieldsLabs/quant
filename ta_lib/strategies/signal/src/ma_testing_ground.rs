use base::prelude::*;
use core::prelude::*;
use shared::{ma_indicator, MovingAverageType};

pub struct MATestingGroundSignal {
    ma: MovingAverageType,
    period: usize,
}

impl MATestingGroundSignal {
    pub fn new(ma: MovingAverageType, period: f32) -> Self {
        Self {
            ma,
            period: period as usize,
        }
    }
}

impl Signal for MATestingGroundSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.period);
        let long_signal = data.low.slt(&ma)
            & data.low.shift(1).slt(&ma.shift(1))
            & data.low.shift(2).slt(&ma.shift(2))
            & data.close.min(&data.open).sgt(&ma)
            & data
                .close
                .shift(1)
                .min(&data.open.shift(1))
                .sgt(&ma.shift(1))
            & data
                .close
                .shift(2)
                .min(&data.open.shift(2))
                .sgt(&ma.shift(2));

        let short_signal = data.high.sgt(&ma)
            & data.high.shift(1).sgt(&ma.shift(1))
            & data.high.shift(2).sgt(&ma.shift(2))
            & data.close.max(&data.open).slt(&ma)
            & data
                .close
                .shift(1)
                .max(&data.open.shift(1))
                .slt(&ma.shift(1))
            & data
                .close
                .shift(2)
                .max(&data.open.shift(2))
                .slt(&ma.shift(2));

        (long_signal, short_signal)
    }
}
