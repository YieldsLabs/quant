use base::prelude::*;
use core::prelude::*;
use shared::{ma_indicator, MovingAverageType};

pub struct MASurpassSignal {
    ma: MovingAverageType,
    period: usize,
}

impl MASurpassSignal {
    pub fn new(ma: MovingAverageType, period: f32) -> Self {
        Self {
            ma,
            period: period as usize,
        }
    }
}

impl Signal for MASurpassSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.period);

        (
            data.open.sgt(&ma)
                & data.close.sgt(&ma)
                & data.low.slt(&ma)
                & data
                    .close
                    .shift(1)
                    .max(&data.open.shift(1))
                    .sgt(&ma.shift(1))
                & data
                    .close
                    .shift(1)
                    .min(&data.open.shift(1))
                    .slt(&ma.shift(1))
                & data
                    .close
                    .shift(2)
                    .max(&data.open.shift(2))
                    .slt(&ma.shift(2)),
            data.open.slt(&ma)
                & data.close.slt(&ma)
                & data.high.sgt(&ma)
                & data
                    .close
                    .shift(1)
                    .min(&data.open.shift(1))
                    .slt(&ma.shift(1))
                & data
                    .close
                    .shift(1)
                    .max(&data.open.shift(1))
                    .sgt(&ma.shift(1))
                & data
                    .close
                    .shift(2)
                    .min(&data.open.shift(2))
                    .sgt(&ma.shift(2)),
        )
    }
}
