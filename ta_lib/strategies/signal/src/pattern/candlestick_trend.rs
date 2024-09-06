use base::prelude::*;
use core::prelude::*;
use indicator::{candlestick_trend_indicator, CandleTrendType};
use timeseries::prelude::*;

const DEFAULT_LOOKBACK: usize = 13;

pub struct CandlestickTrendSignal {
    candle: CandleTrendType,
}

impl CandlestickTrendSignal {
    pub fn new(candle: CandleTrendType) -> Self {
        Self { candle }
    }
}

impl Signal for CandlestickTrendSignal {
    fn lookback(&self) -> usize {
        DEFAULT_LOOKBACK
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        candlestick_trend_indicator(&self.candle, data)
    }
}
