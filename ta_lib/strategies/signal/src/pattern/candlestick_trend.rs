use base::prelude::*;
use core::prelude::*;
use indicator::{candle_trend_indicator, CandleTrendType};

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

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        candle_trend_indicator(&self.candle, data)
    }
}
