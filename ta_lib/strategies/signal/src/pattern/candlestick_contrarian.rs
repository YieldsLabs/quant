use base::prelude::*;
use core::prelude::*;
use indicator::{candlestick_contrarian_indicator, CandleContrarianType};
use timeseries::prelude::*;

const DEFAULT_LOOKBACK: usize = 13;

pub struct CandlestickContrarianSignal {
    candle: CandleContrarianType,
}

impl CandlestickContrarianSignal {
    pub fn new(candle: CandleContrarianType) -> Self {
        Self { candle }
    }
}

impl Signal for CandlestickContrarianSignal {
    fn lookback(&self) -> usize {
        DEFAULT_LOOKBACK
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        candlestick_contrarian_indicator(&self.candle, data)
    }
}
