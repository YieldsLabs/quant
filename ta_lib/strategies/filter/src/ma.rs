use base::{Filter, OHLCVSeries};
use core::series::Series;
use shared::{ma, MovingAverageType};

pub struct MAFilter {
    smoothing: MovingAverageType,
    period: usize,
}

impl MAFilter {
    pub fn new(smoothing: MovingAverageType, period: usize) -> Self {
        Self { smoothing, period }
    }
}

impl Filter for MAFilter {
    fn id(&self) -> String {
        format!("FMA_{}:{}", self.smoothing, self.period)
    }

    fn lookback(&self) -> usize {
        self.period
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma(&self.smoothing, data, self.period);
        let close = Series::from(&data.close);

        (close.gt(&ma), close.lt(&ma))
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
