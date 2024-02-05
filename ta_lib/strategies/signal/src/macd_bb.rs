use base::prelude::*;
use core::prelude::*;
use momentum::macd;
use volatility::bb;

pub struct MACDBBSignal {
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
    signal_period: usize,
    bb_period: usize,
    factor: f32,
}

impl MACDBBSignal {
    pub fn new(
        smooth_type: Smooth,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
        bb_period: f32,
        factor: f32,
    ) -> Self {
        Self {
            smooth_type,
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
        let mut adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        adj_lookback = std::cmp::max(adj_lookback, self.signal_period);
        std::cmp::max(adj_lookback, self.bb_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (macd_line, _, _) = macd(
            &data.close,
            self.smooth_type,
            self.fast_period,
            self.slow_period,
            self.signal_period,
        );

        let (upper_bb, _, lower_bb) = bb(&macd_line, self.smooth_type, self.bb_period, self.factor);

        (
            macd_line.cross_over(&upper_bb),
            macd_line.cross_under(&lower_bb),
        )
    }
}
