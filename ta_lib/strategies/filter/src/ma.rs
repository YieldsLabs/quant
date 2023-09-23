use base::{Filter, OHLCVSeries};
use core::Series;
use shared::{ma_indicator, MovingAverageType};

pub struct MAFilter {
    smoothing: MovingAverageType,
    period: usize,
}

impl MAFilter {
    pub fn new(smoothing: MovingAverageType, period: f32) -> Self {
        Self {
            smoothing,
            period: period as usize,
        }
    }
}

impl Filter for MAFilter {
    fn lookback(&self) -> usize {
        self.period
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.smoothing, data, self.period);
        let close = Series::from(&data.close);

        (close.gt(&ma), close.lt(&ma))
    }
}
