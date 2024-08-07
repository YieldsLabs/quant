use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use volatility::bb;

pub struct BbConfirm {
    smooth: Smooth,
    period: usize,
    factor: f32,
}

impl BbConfirm {
    pub fn new(smooth: Smooth, period: f32, factor: f32) -> Self {
        Self {
            smooth,
            period: period as usize,
            factor,
        }
    }
}

impl Confirm for BbConfirm {
    fn lookback(&self) -> usize {
        self.period
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let close = data.close();
        let prev_close = close.shift(1);
        let (upper_bb, _, lower_bb) = bb(close, self.smooth, self.period, self.factor);

        (
            close.sgt(&lower_bb) & prev_close.slt(&lower_bb),
            close.slt(&upper_bb) & prev_close.sgt(&upper_bb),
        )
    }
}
