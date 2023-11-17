use base::{OHLCVSeries, Signal};
use core::Series;
use momentum::stc;

const LOWER_LINE: f32 = 25.0;
const UPPER_LINE: f32 = 75.0;

pub struct STCUturnSignal {
    fast_period: usize,
    slow_period: usize,
    period: usize,
    factor: f32,
}

impl STCUturnSignal {
    pub fn new(fast_period: f32, slow_period: f32, period: f32, factor: f32) -> Self {
        Self {
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
            period: period as usize,
            factor,
        }
    }
}

impl Signal for STCUturnSignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let stc = stc(
            &data.close,
            self.fast_period,
            self.slow_period,
            self.period,
            self.factor,
        );

        (
            stc.cross_over_line(LOWER_LINE) & stc.cross_over(&stc.shift(2)),
            stc.cross_under_line(UPPER_LINE) & stc.cross_under(&stc.shift(2)),
        )
    }
}
