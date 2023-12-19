use base::{Filter, OHLCVSeries};
use core::{Comparator, Series};
use shared::{stoch_indicator, StochType};

pub struct StochFilter {
    stoch_type: StochType,
    period: usize,
    k_period: usize,
    d_period: usize,
}

impl StochFilter {
    pub fn new(stoch_type: StochType, period: f32, k_period: f32, d_period: f32) -> Self {
        Self {
            stoch_type,
            period: period as usize,
            k_period: k_period as usize,
            d_period: d_period as usize,
        }
    }
}

impl Filter for StochFilter {
    fn lookback(&self) -> usize {
        let adjusted_lookback = std::cmp::max(self.period, self.k_period);
        std::cmp::max(adjusted_lookback, self.d_period)
    }

    fn confirm(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (k, d) = stoch_indicator(
            &self.stoch_type,
            data,
            self.period,
            self.k_period,
            self.d_period,
        );

        (k.sgt(&d), k.slt(&d))
    }
}
