use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use volatility::dch;

pub struct DchStopLoss {
    period: usize,
    factor: f32,
}

impl DchStopLoss {
    pub fn new(period: f32, factor: f32) -> Self {
        Self {
            period: period as usize,
            factor,
        }
    }
}

impl StopLoss for DchStopLoss {
    fn lookback(&self) -> usize {
        self.period
    }

    fn find(&self, data: &OHLCVSeries) -> (Price, Price) {
        let (upper, _, lower) = dch(data.high(), data.low(), self.period);
        let volatility = data.close().std(self.period).highest(self.period) * self.factor;

        (lower - &volatility, upper + &volatility)
    }
}
