use base::{OHLCVSeries, Regime};
use core::Series;
use shared::{ma_indicator, MovingAverageType};

pub struct RibbonFilter {
    smoothing: MovingAverageType,
    first_period: usize,
    second_period: usize,
    third_period: usize,
    fourth_period: usize,
}

impl RibbonFilter {
    pub fn new(
        smoothing: MovingAverageType,
        first_period: f32,
        second_period: f32,
        third_period: f32,
        fourth_period: f32,
    ) -> Self {
        Self {
            smoothing,
            first_period: first_period as usize,
            second_period: second_period as usize,
            third_period: third_period as usize,
            fourth_period: fourth_period as usize,
        }
    }
}

impl Regime for RibbonFilter {
    fn lookback(&self) -> usize {
        let adj_lookback_first = std::cmp::max(self.first_period, self.second_period);
        let adj_lookback_second = std::cmp::max(adj_lookback_first, self.third_period);
        std::cmp::max(adj_lookback_second, self.fourth_period)
    }

    fn apply(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma_first = ma_indicator(&self.smoothing, data, self.first_period);
        let ma_second = ma_indicator(&self.smoothing, data, self.second_period);
        let ma_third = ma_indicator(&self.smoothing, data, self.third_period);
        let ma_fourth = ma_indicator(&self.smoothing, data, self.fourth_period);

        (
            ma_first.gt(&ma_second) & ma_second.gt(&ma_third) & ma_third.gt(&ma_fourth),
            ma_first.lt(&ma_second) & ma_second.lt(&ma_third) & ma_third.lt(&ma_fourth),
        )
    }
}
