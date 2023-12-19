use base::{OHLCVSeries, Price, Signal};
use core::{Comparator, Series};
use trend::supertrend;

pub struct SupertrendPullBackSignal {
    atr_period: usize,
    factor: f32,
}

impl SupertrendPullBackSignal {
    pub fn new(atr_period: f32, factor: f32) -> Self {
        Self {
            atr_period: atr_period as usize,
            factor,
        }
    }
}

impl Signal for SupertrendPullBackSignal {
    fn lookback(&self) -> usize {
        self.atr_period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (direction, trendline) = supertrend(
            &data.hl2(),
            &data.close,
            &data.atr(self.atr_period),
            self.factor,
        );

        let above = data.close.sgt(&trendline);
        let below = data.close.slt(&trendline);

        (
            data.low.sle(&trendline)
                & data.close.sgt(&trendline)
                & below.shift(1)
                & below.shift(2)
                & direction.seq(&1.0),
            data.high.sge(&trendline)
                & data.close.slt(&trendline)
                & above.shift(1)
                & above.shift(2)
                & direction.seq(&-1.0),
        )
    }
}
