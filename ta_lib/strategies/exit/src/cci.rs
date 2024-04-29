use base::prelude::*;
use core::prelude::*;
use momentum::cci;

const CCI_OVERBOUGHT: f32 = 100.0;
const CCI_OVERSOLD: f32 = -100.0;

pub struct CciExit {
    source_type: SourceType,
    smooth_type: Smooth,
    period: usize,
    factor: f32,
    threshold: f32,
}

impl CciExit {
    pub fn new(
        source_type: SourceType,
        smooth_type: Smooth,
        period: f32,
        factor: f32,
        threshold: f32,
    ) -> Self {
        Self {
            source_type,
            smooth_type,
            period: period as usize,
            factor,
            threshold,
        }
    }
}

impl Exit for CciExit {
    fn lookback(&self) -> usize {
        self.period
    }

    fn evaluate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = cci(
            &data.source(self.source_type),
            self.smooth_type,
            self.period,
            self.factor,
        );
        let upper_bound = CCI_OVERBOUGHT - self.threshold;
        let lower_bound = CCI_OVERSOLD + self.threshold;

        (rsi.cross_under(&upper_bound), rsi.cross_over(&lower_bound))
    }
}
