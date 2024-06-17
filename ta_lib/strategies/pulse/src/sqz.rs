use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use volatility::{bb, kch};

pub struct SqzPulse {
    source: SourceType,
    smooth: Smooth,
    period: usize,
    smooth_atr: Smooth,
    period_atr: usize,
    factor_bb: f32,
    factor_kch: f32,
}

impl SqzPulse {
    pub fn new(
        source: SourceType,
        smooth: Smooth,
        period: f32,
        smooth_atr: Smooth,
        period_atr: f32,
        factor_bb: f32,
        factor_kch: f32,
    ) -> Self {
        Self {
            source,
            smooth,
            period: period as usize,
            smooth_atr,
            period_atr: period_atr as usize,
            factor_bb,
            factor_kch,
        }
    }
}

impl Pulse for SqzPulse {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.period_atr)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let source = data.source(self.source);

        let (upbb, _, lwbb) = bb(&source, self.smooth, self.period, self.factor_bb);
        let (upkch, _, lwkch) = kch(
            &source,
            &data.atr(self.smooth_atr, self.period_atr),
            self.smooth,
            self.period,
            self.factor_kch,
        );

        (
            upbb.sgt(&upkch) & lwbb.slt(&lwkch),
            upbb.sgt(&upkch) & lwbb.slt(&lwkch),
        )
    }
}
