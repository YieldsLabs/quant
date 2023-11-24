use base::{OHLCVSeries, Signal};
use core::Series;
use momentum::stc;

const LOWER_LINE: f32 = 25.0;
const UPPER_LINE: f32 = 75.0;

pub struct STCUturnSignal {
    fast_period: usize,
    slow_period: usize,
    cycle: usize,
    d_first: usize,
    d_second: usize,
}

impl STCUturnSignal {
    pub fn new(
        fast_period: f32,
        slow_period: f32,
        cycle: f32,
        d_first: f32,
        d_second: f32,
    ) -> Self {
        Self {
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
            cycle: cycle as usize,
            d_first: d_first as usize,
            d_second: d_second as usize,
        }
    }
}

impl Signal for STCUturnSignal {
    fn lookback(&self) -> usize {
        let adj_lookback_one = std::cmp::max(self.fast_period, self.slow_period);
        let adj_lookback_two = std::cmp::max(adj_lookback_one, self.cycle);
        let adj_lookback_three = std::cmp::max(adj_lookback_two, self.d_first);
        std::cmp::max(adj_lookback_three, self.d_second)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let stc = stc(
            &data.close,
            self.fast_period,
            self.slow_period,
            self.cycle,
            self.d_first,
            self.d_second,
        );

        (
            stc.cross_over_line(LOWER_LINE) & stc.cross_over(&stc.shift(2)),
            stc.cross_under_line(UPPER_LINE) & stc.cross_under(&stc.shift(2)),
        )
    }
}
