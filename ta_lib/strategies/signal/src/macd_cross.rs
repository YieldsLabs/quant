use base::{OHLCVSeries, Signal};
use core::prelude::*;
use shared::{macd_indicator, MACDType};

pub struct MACDCrossSignal {
    macd_type: MACDType,
    fast_period: usize,
    slow_period: usize,
    signal_period: usize,
}

impl MACDCrossSignal {
    pub fn new(
        macd_type: MACDType,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    ) -> Self {
        Self {
            macd_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
            signal_period: signal_period as usize,
        }
    }
}

impl Signal for MACDCrossSignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.signal_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (macd_line, signal_line, _) = macd_indicator(
            &self.macd_type,
            data,
            self.fast_period,
            self.slow_period,
            self.signal_period,
        );

        (
            macd_line.cross_over(&signal_line),
            macd_line.cross_under(&signal_line),
        )
    }
}
