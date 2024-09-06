use base::prelude::*;
use core::prelude::*;
use momentum::tsi;
use timeseries::prelude::*;

pub struct TsiSignalLineSignal {
    source_type: SourceType,
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
    signal_period: usize,
}

impl TsiSignalLineSignal {
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

impl Signal for TsiSignalLineSignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.signal_period)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tsi = tsi(
            &data.source(self.source_type),
            self.smooth_type,
            self.slow_period,
            self.fast_period,
        );
        let signal_line = tsi.smooth(self.smooth_type, self.signal_period);

        (tsi.cross_over(&signal_line), tsi.cross_under(&signal_line))
    }
}
