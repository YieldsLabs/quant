use base::prelude::*;
use core::prelude::*;
use momentum::macd;
use timeseries::prelude::*;

pub struct MacdColorSwitchSignal {
    source_type: SourceType,
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
    signal_period: usize,
}

impl MacdColorSwitchSignal {
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

impl Signal for MacdColorSwitchSignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.signal_period)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (_, _, histogram) = macd(
            &data.source(self.source_type),
            self.smooth_type,
            self.fast_period,
            self.slow_period,
            self.signal_period,
        );

        let prev_histogram = histogram.shift(1);
        let back_2_histogram = histogram.shift(2);
        let back_3_histogram = histogram.shift(3);

        (
            histogram.slt(&ZERO)
                & histogram.sgt(&prev_histogram)
                & prev_histogram.slt(&back_2_histogram)
                & back_2_histogram.slt(&back_3_histogram),
            histogram.sgt(&ZERO)
                & histogram.slt(&prev_histogram)
                & prev_histogram.sgt(&back_2_histogram)
                & back_2_histogram.sgt(&back_3_histogram),
        )
    }
}
