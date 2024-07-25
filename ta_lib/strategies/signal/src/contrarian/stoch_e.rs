use base::prelude::*;
use core::prelude::*;
use momentum::stochosc;
use timeseries::prelude::*;

const STOCH_UPPER_BARRIER: f32 = 95.0;
const STOCH_LOWER_BARRIER: f32 = 5.0;

pub struct StochESignal {
    source: SourceType,
    smooth: Smooth,
    period: usize,
    period_k: usize,
    period_d: usize,
    threshold: f32,
}

impl StochESignal {
    pub fn new(
        source: SourceType,
        smooth: Smooth,
        period: f32,
        period_k: f32,
        period_d: f32,
        threshold: f32,
    ) -> Self {
        Self {
            source,
            smooth,
            period: period as usize,
            period_k: period_k as usize,
            period_d: period_d as usize,
            threshold,
        }
    }
}

impl Signal for StochESignal {
    fn lookback(&self) -> usize {
        std::cmp::max(std::cmp::max(self.period, self.period_k), self.period_d)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (k, _) = stochosc(
            &data.source(self.source),
            data.high(),
            data.low(),
            self.smooth,
            self.period,
            self.period_k,
            self.period_d,
        );

        let lower_barrier = STOCH_LOWER_BARRIER + self.threshold;
        let upper_barrier = STOCH_UPPER_BARRIER - self.threshold;

        let prev_k = k.shift(1);

        (
            k.sgt(&lower_barrier) & prev_k.slt(&lower_barrier),
            k.slt(&upper_barrier) & prev_k.sgt(&upper_barrier),
        )
    }
}
