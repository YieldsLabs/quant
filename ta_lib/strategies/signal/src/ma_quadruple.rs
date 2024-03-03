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

        let prev_ma = ma.shift(1);
        let back_2_ma = ma.shift(2);
        let back_3_ma = ma.shift(3);

        let prev_close = data.close.shift(1);
        let back_2_close = data.close.shift(2);
        let back_3_close = data.close.shift(3);

        (
            data.low.slt(&ma)
                & data.close.sgt(&ma)
                & data.low.shift(1).slt(&prev_ma)
                & prev_close.sgt(&prev_ma)
                & data.low.shift(2).slt(&back_2_ma)
                & back_2_close.sgt(&back_2_ma)
                & data.low.shift(3).slt(&back_3_ma)
                & back_3_close.sgt(&back_3_ma),
            data.high.sgt(&ma)
                & data.close.slt(&ma)
                & data.high.shift(1).sgt(&prev_ma)
                & prev_close.slt(&prev_ma)
                & data.high.shift(2).sgt(&back_2_ma)
                & back_2_close.slt(&back_2_ma)
                & data.high.shift(3).sgt(&back_3_ma)
                & back_3_close.slt(&back_3_ma),
        )
    }
}
