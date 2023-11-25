use base::{Filter, OHLCVSeries};
use core::Series;
use shared::{macd_indicator, MACDType};

const MACD_ZERO: f32 = 0.0;

pub struct MACDFilter {
    macd_type: MACDType,
    fast_period: usize,
    slow_period: usize,
    signal_smoothing: usize,
}

impl MACDFilter {
    pub fn new(
        macd_type: MACDType,
        fast_period: f32,
        slow_period: f32,
        signal_smoothing: f32,
    ) -> Self {
        Self {
            macd_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
            signal_smoothing: signal_smoothing as usize,
        }
    }
}

impl Filter for MACDFilter {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.signal_smoothing)
    }

    fn confirm(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (_, _, histogram) = macd_indicator(
            &self.macd_type,
            data,
            self.fast_period,
            self.slow_period,
            self.signal_smoothing,
        );

        (histogram.sgt(MACD_ZERO), histogram.slt(MACD_ZERO))
    }
}
