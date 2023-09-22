use base::{OHLCVSeries, Signal};
use core::Series;
use shared::{trend_candle_indicator, TrendCandleType};

const DEFAULT_LOOKBACK: usize = 13;

pub struct TrendCandleSignal {
    candle: TrendCandleType,
}

impl TrendCandleSignal {
    pub fn new(candle: TrendCandleType) -> Self {
        Self { candle }
    }
}

impl Signal for TrendCandleSignal {
    fn id(&self) -> String {
        format!("TRENDCANDLE_{}", self.candle)
    }

    fn lookback(&self) -> usize {
        DEFAULT_LOOKBACK
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        trend_candle_indicator(&self.candle, data)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
