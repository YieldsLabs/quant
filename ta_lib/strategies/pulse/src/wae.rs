use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use volatility::bb;

pub struct WaePulse {
    source: SourceType,
    smooth: Smooth,
    period_fast: usize,
    period_slow: usize,
    smooth_bb: Smooth,
    period_bb: usize,
    factor: f32,
    strength: f32,
}

impl WaePulse {
    pub fn new(
        source: SourceType,
        smooth: Smooth,
        period_fast: f32,
        period_slow: f32,
        smooth_bb: Smooth,
        period_bb: f32,
        factor: f32,
        strength: f32,
    ) -> Self {
        Self {
            source,
            smooth,
            period_fast: period_fast as usize,
            period_slow: period_slow as usize,
            smooth_bb,
            period_bb: period_bb as usize,
            factor,
            strength,
        }
    }
}

impl Pulse for WaePulse {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.period_fast, self.period_slow);
        std::cmp::max(adj_lookback, self.period_bb)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let source = data.source(self.source);

        let (upper_bb, _, lower_bb) = bb(&source, self.smooth_bb, self.period_bb, self.factor);

        let e = upper_bb - lower_bb;

        let diff =
            self.strength * source.spread_diff(self.smooth, self.period_fast, self.period_slow, 1);

        let zero = Series::zero(data.len());

        let up = iff!(diff.sgte(&ZERO), diff, zero);
        let down = iff!(diff.slt(&ZERO), diff.negate(), zero);

        (
            up.sgt(&up.shift(1)) & up.sgt(&e),
            down.sgt(&down.shift(1)) & down.sgt(&e),
        )
    }
}
