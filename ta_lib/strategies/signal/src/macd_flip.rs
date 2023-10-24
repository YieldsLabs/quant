use base::{OHLCVSeries, Signal};
use core::Series;
use shared::{macd_indicator, MACDType};

const ZERO_LINE: f32 = 00.0;

pub struct MACDFlipSignal {
    macd_type: MACDType,
    fast_period: usize,
    slow_period: usize,
    signal_smoothing: usize,
}

impl MACDFlipSignal {
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

impl Signal for MACDFlipSignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.signal_smoothing)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (macd_line, _, _) = macd_indicator(
            &self.macd_type,
            data,
            self.fast_period,
            self.slow_period,
            self.signal_smoothing,
        );

        (
            macd_line.cross_over_line(ZERO_LINE),
            macd_line.cross_under_line(ZERO_LINE),
        )
    }
}
