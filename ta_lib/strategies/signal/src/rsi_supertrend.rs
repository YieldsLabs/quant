use base::prelude::*;
use core::prelude::*;
use momentum::rsi;
use trend::supertrend;

const RSI_UPPER_BARRIER: f32 = 75.0;
const RSI_LOWER_BARRIER: f32 = 25.0;
const RSI_NEUTRALITY: f32 = 50.0;

pub struct RSISupertrendSignal {
    smooth_type: Smooth,
    rsi_period: usize,
    threshold: f32,
    atr_period: usize,
    factor: f32,
}

impl RSISupertrendSignal {
    pub fn new(
        smooth_type: Smooth,
        rsi_period: f32,
        threshold: f32,
        atr_period: f32,
        factor: f32,
    ) -> Self {
        Self {
            smooth_type,
            rsi_period: rsi_period as usize,
            threshold,
            atr_period: atr_period as usize,
            factor,
        }
    }
}

impl Signal for RSISupertrendSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.rsi_period, self.atr_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.close, self.smooth_type, self.rsi_period);
        let (direction, _) = supertrend(
            &data.hl2(),
            &data.close,
            &data.atr(self.atr_period),
            self.factor,
        );
        let lower_barrier = RSI_LOWER_BARRIER + self.threshold;
        let upper_barrier = RSI_UPPER_BARRIER - self.threshold;
        let lower_neutrality = RSI_NEUTRALITY - self.threshold;
        let upper_neutrality = RSI_NEUTRALITY + self.threshold;

        (
            direction.seq(&1.0)
                & rsi.sgt(&RSI_NEUTRALITY)
                & rsi.slt(&upper_barrier)
                & rsi.shift(1).sgt(&lower_neutrality)
                & rsi.shift(2).sgt(&lower_neutrality)
                & rsi.shift(3).sgt(&lower_neutrality),
            direction.seq(&-1.0)
                & rsi.slt(&RSI_NEUTRALITY)
                & rsi.sgt(&lower_barrier)
                & rsi.shift(1).slt(&upper_neutrality)
                & rsi.shift(2).slt(&upper_neutrality)
                & rsi.shift(3).slt(&upper_neutrality),
        )
    }
}
