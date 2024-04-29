use base::prelude::*;
use core::prelude::*;
use momentum::macd;

pub struct MacdZeroCrossSignal {
    source_type: SourceType,
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
    signal_period: usize,
}

impl MacdZeroCrossSignal {
    pub fn new(
        source_type: SourceType,
        smooth_type: Smooth,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    ) -> Self {
        Self {
            source_type,
            smooth_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
            signal_period: signal_period as usize,
        }
    }
}

impl Signal for MacdZeroCrossSignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.signal_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (macd_line, _, _) = macd(
            &data.source(self.source_type),
            self.smooth_type,
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
