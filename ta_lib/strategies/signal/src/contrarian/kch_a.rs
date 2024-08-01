use base::prelude::*;
use channel::a;
use core::prelude::*;
use timeseries::prelude::*;
use volatility::kch;

pub struct KchASignal {
    source: SourceType,
    smooth: Smooth,
    period: usize,
    smooth_atr: Smooth,
    period_atr: usize,
    factor: f32,
}

impl KchASignal {
    pub fn new(
        source: SourceType,
        smooth: Smooth,
        period: f32,
        smooth_atr: Smooth,
        period_atr: f32,
        factor: f32,
    ) -> Self {
        Self {
            source,
            smooth,
            period: period as usize,
            smooth_atr,
            period_atr: period_atr as usize,
            factor,
        }
    }
}

impl Signal for KchASignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.period_atr)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let source = data.source(self.source);
        let (upper, _, lower) = kch(
            &source,
            self.smooth,
            &data.atr(self.smooth_atr, self.period_atr),
            self.period,
            self.factor,
        );

        a!(upper, lower, source)
    }
}
