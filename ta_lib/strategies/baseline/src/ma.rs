use base::prelude::*;
use core::prelude::*;
use indicator::{ma_indicator, MovingAverageType};
use timeseries::prelude::*;

const DEFAULT_ATR_LOOKBACK: Period = 14;
const DEFAULT_ATR_FACTOR: Scalar = 1.2;
const DEFAULT_ATR_SMOOTH: Smooth = Smooth::EMA;

pub struct MaBaseLine {
    source: SourceType,
    ma: MovingAverageType,
    period: usize,
}

impl MaBaseLine {
    pub fn new(source: SourceType, ma: MovingAverageType, period: f32) -> Self {
        Self {
            source,
            ma,
            period: period as usize,
        }
    }
}

impl BaseLine for MaBaseLine {
    fn lookback(&self) -> usize {
        std::cmp::max(DEFAULT_ATR_LOOKBACK, self.period)
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.source, self.period);
        let close = data.close();

        let dist = (&ma - close).abs();
        let atr = data.atr(DEFAULT_ATR_SMOOTH, DEFAULT_ATR_LOOKBACK) * DEFAULT_ATR_FACTOR;

        (
            close.sgt(&ma) & dist.slt(&atr),
            close.slt(&ma) & dist.slt(&atr),
        )
    }

    fn close(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.source, self.period);
        let close = data.close();

        (close.cross_under(&ma), close.cross_over(&ma))
    }
}
