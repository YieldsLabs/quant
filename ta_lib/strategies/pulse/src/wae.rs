use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use volatility::bb;

pub struct WaePulse {
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
    smooth_bb: Smooth,
    bb_period: usize,
    factor: f32,
    strength: f32,
}

impl WaePulse {
    pub fn new(
        smooth_type: Smooth,
        fast_period: f32,
        slow_period: f32,
        smooth_bb: Smooth,
        bb_period: f32,
        factor: f32,
        strength: f32,
    ) -> Self {
        Self {
            smooth_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
            smooth_bb,
            bb_period: bb_period as usize,
            factor,
            strength,
        }
    }
}

impl Pulse for WaePulse {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.bb_period)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (upper_bb, _, lower_bb) = bb(data.close(), self.smooth_bb, self.bb_period, self.factor);
        let e = upper_bb - lower_bb;

        let prev_close = data.close().shift(1);

        let macd_line = data.close().smooth(self.smooth_type, self.fast_period)
            - data.close().smooth(self.smooth_type, self.slow_period);
        let prev_macd_line = prev_close.smooth(self.smooth_type, self.fast_period)
            - prev_close.smooth(self.smooth_type, self.slow_period);
        let t = (macd_line - prev_macd_line) * self.strength;

        let zero = Series::zero(data.len());

        let up = iff!(t.sgte(&ZERO), t, zero);
        let down = iff!(t.slt(&ZERO), t.negate(), zero);

        (
            up.sgt(&up.shift(1)) & up.sgt(&e),
            down.sgt(&down.shift(1)) & down.sgt(&e),
        )
    }
}
