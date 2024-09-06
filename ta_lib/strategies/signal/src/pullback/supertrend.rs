use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use trail::p;
use trend::supertrend;

pub struct SupertrendPullbackSignal {
    source: SourceType,
    smooth_atr: Smooth,
    period_atr: usize,
    factor: f32,
}

impl SupertrendPullbackSignal {
    pub fn new(source: SourceType, smooth_atr: Smooth, period_atr: f32, factor: f32) -> Self {
        Self {
            source,
            smooth_atr,
            period_atr: period_atr as usize,
            factor,
        }
    }
}

impl Signal for SupertrendPullbackSignal {
    fn lookback(&self) -> usize {
        self.period_atr
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let source = data.source(self.source);
        let atr = data.atr(self.smooth_atr, self.period_atr);
        let close = data.close();

        let (_, trend) = supertrend(&source, close, &atr, self.factor);

        p!(trend, data.high(), data.low(), close)
    }
}
