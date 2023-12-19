use base::{Filter, OHLCVSeries};
use core::{Comparator, Series};
use trend::dpo;

const DPO_FILTER: f32 = 0.0;

pub struct DPOFilter {
    period: usize,
}

impl DPOFilter {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Filter for DPOFilter {
    fn lookback(&self) -> usize {
        self.period
    }

    fn confirm(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let dpo = dpo(&data.close, self.period);

        (dpo.sgt(&DPO_FILTER), dpo.slt(&DPO_FILTER))
    }
}
