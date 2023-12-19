use base::{Filter, OHLCVSeries};
use core::{Comparator, Series};
use shared::{macd_indicator, MACDType};

pub struct EISFilter {
    macd_type: MACDType,
    fast_period: usize,
    slow_period: usize,
    signal_smoothing: usize,
    signal_period: usize,
}

impl EISFilter {
    pub fn new(
        macd_type: MACDType,
        fast_period: f32,
        slow_period: f32,
        signal_smoothing: f32,
        signal_period: f32,
    ) -> Self {
        Self {
            macd_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
            signal_smoothing: signal_smoothing as usize,
            signal_period: signal_period as usize,
        }
    }
}

impl Filter for EISFilter {
    fn lookback(&self) -> usize {
        let adj_lookback_one = std::cmp::max(self.fast_period, self.slow_period);
        let adj_lookback_two = std::cmp::max(adj_lookback_one, self.signal_smoothing);
        std::cmp::max(adj_lookback_two, self.signal_period)
    }

    fn confirm(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (_, _, histogram) = macd_indicator(
            &self.macd_type,
            data,
            self.fast_period,
            self.slow_period,
            self.signal_smoothing,
        );
        let signal = data.close.ema(self.signal_period);

        (
            signal.sgt(&signal.shift(1)) & histogram.sgt(&histogram.shift(1)),
            signal.slt(&signal.shift(1)) & histogram.slt(&histogram.shift(1)),
        )
    }
}
