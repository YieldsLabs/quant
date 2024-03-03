use base::prelude::*;
use core::prelude::*;
use momentum::macd;

const ZERO_LINE: f32 = 0.0;

pub struct MACDColorSwitchSignal {
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
    signal_period: usize,
}

impl MACDColorSwitchSignal {
    pub fn new(
        smooth_type: Smooth,
        fast_period: f32,
        slow_period: f32,
        signal_period: f32,
    ) -> Self {
        Self {
            smooth_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
            signal_period: signal_period as usize,
        }
    }
}

impl Signal for MACDColorSwitchSignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.signal_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (_, _, histogram) = macd(
            &data.close,
            self.smooth_type,
            self.fast_period,
            self.slow_period,
            self.signal_period,
        );

        let prev_histogram = histogram.shift(1);
        let back_2_histogram = histogram.shift(2);
        let back_3_histogram = histogram.shift(3);

        (
            histogram.slt(&ZERO_LINE)
                & histogram.sgt(&prev_histogram)
                & prev_histogram.slt(&back_2_histogram)
                & back_2_histogram.slt(&back_3_histogram),
            histogram.sgt(&ZERO_LINE)
                & histogram.slt(&prev_histogram)
                & prev_histogram.sgt(&back_2_histogram)
                & back_2_histogram.sgt(&back_3_histogram),
        )
    }
}
