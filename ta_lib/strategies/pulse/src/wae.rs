use base::prelude::*;
use core::prelude::*;
use volatility::bb;

pub struct WaePulse {
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
    smooth_bb: Smooth,
    bb_period: usize,
    factor: f32,
    strength: f32,
    atr_period: usize,
    dz_factor: f32,
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
        atr_period: f32,
        dz_factor: f32,
    ) -> Self {
        Self {
            smooth_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
            smooth_bb,
            bb_period: bb_period as usize,
            factor,
            strength,
            atr_period: atr_period as usize,
            dz_factor,
        }
    }
}

impl Pulse for WaePulse {
    fn lookback(&self) -> usize {
        let mut adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        adj_lookback = std::cmp::max(adj_lookback, self.bb_period);
        std::cmp::max(adj_lookback, self.atr_period)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let dz = data.atr(self.atr_period, Smooth::SMMA) * self.dz_factor;

        let (upper_bb, _, lower_bb) = bb(&data.close, self.smooth_bb, self.bb_period, self.factor);
        let e = upper_bb - lower_bb;

        let prev_close = data.close.shift(1);

        let macd_line = data.close.smooth(self.smooth_type, self.fast_period)
            - data.close.smooth(self.smooth_type, self.slow_period);
        let prev_macd_line = prev_close.smooth(self.smooth_type, self.fast_period)
            - prev_close.smooth(self.smooth_type, self.slow_period);
        let t = (macd_line - prev_macd_line) * self.strength;

        let zero = Series::zero(data.close.len());

        let up = iff!(t.sgte(&ZERO), t, zero);
        let down = iff!(t.slt(&ZERO), t.negate(), zero);

        (
            up.sgt(&up.shift(1)) & up.sgt(&e) & up.sgt(&dz),
            down.sgt(&down.shift(1)) & down.sgt(&e) & down.sgt(&dz),
        )
    }
}
