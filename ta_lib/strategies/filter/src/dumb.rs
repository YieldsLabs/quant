use base::{Filter, OHLCVSeries};
use core::series::Series;

pub struct DumbFilter {
    period: usize,
}

impl DumbFilter {
    pub fn new(period: usize) -> Self {
        Self { period }
    }
}

impl Filter for DumbFilter {
    fn id(&self) -> String {
        format!("FDUMB")
    }

    fn lookback(&self) -> usize {
        self.period
    }

    fn entry(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (
            Series::empty(1).nz(Some(1.0)).into(),
            Series::empty(1).nz(Some(1.0)).into(),
        )
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (
            Series::empty(1).nz(Some(1.0)).into(),
            Series::empty(1).nz(Some(1.0)).into(),
        )
    }
}
