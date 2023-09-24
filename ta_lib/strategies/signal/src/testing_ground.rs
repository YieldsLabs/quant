use base::{OHLCVSeries, Signal};
use core::Series;
use shared::{ma_indicator, MovingAverageType};

pub struct TestingGroundSignal {
    smoothing: MovingAverageType,
    smoothing_period: usize,
}

impl TestingGroundSignal {
    pub fn new(smoothing: MovingAverageType, smoothing_period: f32) -> Self {
        Self {
            smoothing,
            smoothing_period: smoothing_period as usize,
        }
    }
}

impl Signal for TestingGroundSignal {
    fn lookback(&self) -> usize {
        self.smoothing_period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.smoothing, data, self.smoothing_period);

        let open = Series::from(&data.open);
        let high = Series::from(&data.high);
        let low = Series::from(&data.low);
        let close = Series::from(&data.close);

        let long_signal = low.lt(&ma)
            & low.shift(1).lt(&ma.shift(1))
            & low.shift(2).lt(&ma.shift(2))
            & close.min(&open).gt(&ma)
            & close.shift(1).min(&open.shift(1)).gt(&ma.shift(1))
            & close.shift(2).min(&open.shift(2)).gt(&ma.shift(2));

        let short_signal = high.gt(&ma)
            & high.shift(1).gt(&ma.shift(1))
            & high.shift(2).gt(&ma.shift(2))
            & close.max(&open).lt(&ma)
            & close.shift(1).max(&open.shift(1)).lt(&ma.shift(1))
            & close.shift(2).max(&open.shift(2)).lt(&ma.shift(2));

        (long_signal, short_signal)
    }
}
