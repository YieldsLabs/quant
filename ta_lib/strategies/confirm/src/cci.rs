use base::prelude::*;
use core::prelude::*;
use momentum::cci;
use timeseries::prelude::*;

const CCI_UPPER_NEUTRALITY: f32 = 50.;
const CCI_LOWER_NEUTRALITY: f32 = -50.;
const CCI_UPPER_BARRIER: f32 = 100.;
const CCI_LOWER_BARRIER: f32 = -100.;

pub struct CciConfirm {
    source: SourceType,
    period: usize,
    factor: f32,
    smooth: Smooth,
    period_smooth: usize,
}

impl CciConfirm {
    pub fn new(
        source: SourceType,
        period: f32,
        factor: f32,
        smooth: Smooth,
        period_smooth: f32,
    ) -> Self {
        Self {
            source,
            period: period as usize,
            factor,
            smooth,
            period_smooth: period_smooth as usize,
        }
    }
}

impl Confirm for CciConfirm {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.period_smooth)
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let cci = cci(&data.source(self.source), self.period, self.factor)
            .smooth(self.smooth, self.period_smooth);

        (
            cci.sgt(&CCI_UPPER_NEUTRALITY) & cci.slt(&CCI_UPPER_BARRIER),
            cci.slt(&CCI_LOWER_NEUTRALITY) & cci.sgt(&CCI_LOWER_BARRIER),
        )
    }
}
