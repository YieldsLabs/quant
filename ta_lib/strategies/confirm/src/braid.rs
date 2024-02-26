use base::prelude::*;
use core::prelude::*;

const ONE: f32 = 1.;
const MINUS_ONE: f32 = -1.;

pub struct BraidConfirm {
    smooth_type: Smooth,
    period_one: usize,
    period_two: usize,
    period_three: usize,
    strength: f32,
    atr_period: usize,
}

impl BraidConfirm {
    pub fn new(
        smooth_type: Smooth,
        period_one: f32,
        period_two: f32,
        period_three: f32,
        strength: f32,
        atr_period: f32,
    ) -> Self {
        Self {
            smooth_type,
            period_one: period_one as usize,
            period_two: period_two as usize,
            period_three: period_three as usize,
            strength,
            atr_period: atr_period as usize,
        }
    }
}

impl Confirm for BraidConfirm {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.period_one, self.period_two);
        std::cmp::max(adj_lookback, self.period_three)
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma_one = data.close.smooth(self.smooth_type, self.period_one);
        let ma_two = data.open.smooth(self.smooth_type, self.period_two);
        let ma_three = data.close.smooth(self.smooth_type, self.period_three);
        let filter = data.atr(self.atr_period, Smooth::SMMA) * self.strength / 100.0;

        let max = ma_one.max(&ma_two).max(&ma_three);
        let min = ma_one.min(&ma_two).min(&ma_three);

        let diff = max - min;

        let len = data.close.len();

        let regime = iff!(
            ma_one.sgt(&ma_two),
            Series::one(len),
            iff!(
                ma_one.slt(&ma_two),
                Series::fill(MINUS_ONE, len),
                Series::zero(len)
            )
        );

        (
            regime.seq(&ONE) & diff.sgt(&filter),
            regime.seq(&MINUS_ONE) & diff.sgt(&filter),
        )
    }
}
