use base::prelude::*;
use core::prelude::*;
use indicator::{candlestick_reversal_indicator, CandleReversalType};
use timeseries::prelude::*;

const DEFAULT_LOOKBACK: usize = 200;

pub struct CandlestickReversalSignal {
    candle: CandleReversalType,
}

impl CandlestickReversalSignal {
    pub fn new(candle: CandleReversalType) -> Self {
        Self { candle }
    }
}

impl Signal for CandlestickReversalSignal {
    fn lookback(&self) -> usize {
        DEFAULT_LOOKBACK
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        candlestick_reversal_indicator(&self.candle, data)
    }
}
