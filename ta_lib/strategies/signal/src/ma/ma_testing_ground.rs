use base::prelude::*;
use core::prelude::*;
use indicator::{ma_indicator, MovingAverageType};
use timeseries::prelude::*;

pub struct MaTestingGroundSignal {
    source_type: SourceType,
    ma: MovingAverageType,
    period: usize,
}

impl MaTestingGroundSignal {
    pub fn new(source_type: SourceType, ma: MovingAverageType, period: f32) -> Self {
        Self {
            source_type,
            ma,
            period: period as usize,
        }
    }
}

impl Signal for MaTestingGroundSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.source_type, self.period);

        let prev_ma = ma.shift(1);
        let back_2_ma = ma.shift(2);

        let prev_close = data.close().shift(1);
        let back_2_close = data.close().shift(2);

        let prev_open = data.open().shift(1);
        let back_2_open = data.open().shift(2);

        (
            data.low().slt(&ma)
                & data.low().shift(1).slt(&prev_ma)
                & data.low().shift(2).slt(&back_2_ma)
                & data.close().min(data.open()).sgt(&ma)
                & prev_close.min(&prev_open).sgt(&prev_ma)
                & back_2_close.min(&back_2_open).sgt(&back_2_ma),
            data.high().sgt(&ma)
                & data.high().shift(1).sgt(&prev_ma)
                & data.high().shift(2).sgt(&back_2_ma)
                & data.close().max(data.open()).slt(&ma)
                & prev_close.max(&prev_open).slt(&prev_ma)
                & back_2_close.max(&back_2_open).slt(&back_2_ma),
        )
    }
}
