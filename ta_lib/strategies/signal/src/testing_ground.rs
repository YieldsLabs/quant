use base::{OHLCVSeries, Signal};
use core::{Extremum, Series};
use shared::{ma_indicator, MovingAverageType};

pub struct TestingGroundSignal {
    smoothing: MovingAverageType,
    period: usize,
}

impl TestingGroundSignal {
    pub fn new(smoothing: MovingAverageType, period: f32) -> Self {
        Self {
            smoothing,
            period: period as usize,
        }
    }
}

impl Signal for TestingGroundSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.smoothing, data, self.period);
        let long_signal = data.low.lt(&ma)
            & data.low.shift(1).lt(&ma.shift(1))
            & data.low.shift(2).lt(&ma.shift(2))
            & data.close.min(&data.open).gt(&ma)
            & data
                .close
                .shift(1)
                .min(&data.open.shift(1))
                .gt(&ma.shift(1))
            & data
                .close
                .shift(2)
                .min(&data.open.shift(2))
                .gt(&ma.shift(2));

        let short_signal = data.high.gt(&ma)
            & data.high.shift(1).gt(&ma.shift(1))
            & data.high.shift(2).gt(&ma.shift(2))
            & data.close.max(&data.open).lt(&ma)
            & data
                .close
                .shift(1)
                .max(&data.open.shift(1))
                .lt(&ma.shift(1))
            & data
                .close
                .shift(2)
                .max(&data.open.shift(2))
                .lt(&ma.shift(2));

        (long_signal, short_signal)
    }
}
