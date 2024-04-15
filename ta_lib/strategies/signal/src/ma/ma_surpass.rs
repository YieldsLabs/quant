use base::prelude::*;
use core::prelude::*;
use indicator::{ma_indicator, MovingAverageType};

pub struct MaSurpassSignal {
    ma: MovingAverageType,
    period: usize,
}

impl MaSurpassSignal {
    pub fn new(ma: MovingAverageType, period: f32) -> Self {
        Self {
            ma,
            period: period as usize,
        }
    }
}

impl Signal for MaSurpassSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.period);

        let prev_ma = ma.shift(1);
        let back_2_ma = ma.shift(2);

        let prev_open = data.open.shift(1);
        let back_2_open = data.open.shift(2);

        let prev_close = data.close.shift(1);
        let back_2_close = data.close.shift(2);

        let prev_max = prev_close.max(&prev_open);
        let prev_min = prev_close.min(&prev_open);

        (
            data.open.sgt(&ma)
                & data.close.sgt(&ma)
                & data.low.slt(&ma)
                & prev_max.sgt(&prev_ma)
                & prev_min.slt(&prev_ma)
                & back_2_close.max(&back_2_open).slt(&back_2_ma),
            data.open.slt(&ma)
                & data.close.slt(&ma)
                & data.high.sgt(&ma)
                & prev_min.slt(&prev_ma)
                & prev_max.sgt(&prev_ma)
                & back_2_close.min(&back_2_open).sgt(&back_2_ma),
        )
    }
}
