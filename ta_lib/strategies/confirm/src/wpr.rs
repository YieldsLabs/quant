use base::prelude::*;
use core::prelude::*;
use momentum::pr;
use timeseries::prelude::*;

const WRP_UPPER_BARRIER: f32 = -20.;
const WRP_LOWER_BARRIER: f32 = -80.;

pub struct WprConfirm {
    source_type: SourceType,
    period: usize,
    threshold: f32,
}

impl WprConfirm {
    pub fn new(source_type: SourceType, period: f32, threshold: f32) -> Self {
        Self {
            source_type,
            period: period as usize,
            threshold,
        }
    }
}

impl Confirm for WprConfirm {
    fn lookback(&self) -> usize {
        self.period
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let wrp = pr(
            &data.source(self.source_type),
            data.high(),
            data.low(),
            self.period,
        );

        let upper_barrier = WRP_UPPER_BARRIER + self.threshold;
        let lower_barrier = WRP_LOWER_BARRIER - self.threshold;

        (wrp.sgt(&upper_barrier), wrp.slt(&lower_barrier))
    }
}
