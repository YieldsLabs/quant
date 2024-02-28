use base::prelude::*;
use core::prelude::*;
use shared::{ma_indicator, MovingAverageType};

pub struct MAQuadrupleSignal {
    ma: MovingAverageType,
    period: usize,
}

impl MAQuadrupleSignal {
    pub fn new(ma: MovingAverageType, period: f32) -> Self {
        Self {
            ma,
            period: period as usize,
        }
    }
}

impl Signal for MAQuadrupleSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.period);

        (
            data.low.slt(&ma)
                & data.close.sgt(&ma)
                & data.low.shift(1).slt(&ma.shift(1))
                & data.close.shift(1).sgt(&ma.shift(1))
                & data.low.shift(2).slt(&ma.shift(2))
                & data.close.shift(2).sgt(&ma.shift(2))
                & data.low.shift(3).slt(&ma.shift(3))
                & data.close.shift(3).sgt(&ma.shift(3)),
            data.high.sgt(&ma)
                & data.close.slt(&ma)
                & data.high.shift(1).sgt(&ma.shift(1))
                & data.close.shift(1).slt(&ma.shift(1))
                & data.high.shift(2).sgt(&ma.shift(2))
                & data.close.shift(2).slt(&ma.shift(2))
                & data.high.shift(3).sgt(&ma.shift(3))
                & data.close.shift(3).slt(&ma.shift(3)),
        )
    }
}
