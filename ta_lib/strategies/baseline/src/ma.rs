use base::prelude::*;
use core::prelude::*;
use shared::{ma_indicator, MovingAverageType};

const DEFAULT_ATR_LOOKBACK: usize = 14;
const DEFAULT_ATR_FACTOR: f32 = 1.382;

pub struct MABaseLine {
    ma: MovingAverageType,
    period: usize,
}

impl MABaseLine {
    pub fn new(ma: MovingAverageType, period: f32) -> Self {
        Self {
            ma,
            period: period as usize,
        }
    }
}

impl BaseLine for MABaseLine {
    fn lookback(&self) -> usize {
        std::cmp::max(DEFAULT_ATR_LOOKBACK, self.period)
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.period);

        let dist = (&ma - &data.close).abs();
        let atr = data.atr(DEFAULT_ATR_LOOKBACK, Smooth::SMMA) * DEFAULT_ATR_FACTOR;

        (
            ma.slt(&data.close) & dist.slt(&atr),
            ma.sgt(&data.close) & dist.slt(&atr),
        )
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.period);

        (data.close.cross_over(&ma), data.close.cross_under(&ma))
    }
}
