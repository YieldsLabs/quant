use base::prelude::*;
use core::prelude::*;
use momentum::macd;


pub struct MACDBBSignal {
    fast_period: usize,
    slow_period: usize,
    signal_period: usize,
    bb_period: usize,
    factor: f32,
}

impl MACDBBSignal {
    pub fn new(fast_period: f32, slow_period: f32, signal_period: f32, bb_period: f32, factor: f32) -> Self {
        Self {
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
            signal_period: signal_period as usize,
            bb_period: bb_period as usize,
            factor,
        }
    }
}

impl Signal for MACDBBSignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.signal_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (macd_line, _, _) = macd(
            &data.close,
            self.fast_period,
            self.slow_period,
            self.signal_period,
        );

        (
            macd_line.cross_over(&ZERO_LINE),
            macd_line.cross_under(&ZERO_LINE),
        )
    }
}
