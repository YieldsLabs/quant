use base::prelude::*;
use core::prelude::*;
use momentum::rsi;
use trend::supertrend;

const RSI_UPPER_BARRIER: f32 = 75.0;
const RSI_LOWER_BARRIER: f32 = 25.0;

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
            &data.atr(self.atr_period, Smooth::SMMA),
            self.factor,
        );
        let lower_barrier = RSI_LOWER_BARRIER + self.threshold;
        let upper_barrier = RSI_UPPER_BARRIER - self.threshold;
        let lower_neutrality = NEUTRALITY_LINE - self.threshold;
        let upper_neutrality = NEUTRALITY_LINE + self.threshold;

        let prev_direction = direction.shift(1);
        let back_2_direction = direction.shift(2);
        let back_3_direction = direction.shift(3);

        let prev_rsi = rsi.shift(1);
        let back_2_rsi = rsi.shift(2);
        let back_3_rsi = rsi.shift(3);

        (
            direction.seq(&ONE)
                & prev_direction.seq(&ONE)
                & back_2_direction.seq(&ONE)
                & back_3_direction.seq(&ONE)
                & rsi.sgt(&NEUTRALITY_LINE)
                & rsi.slt(&upper_barrier)
                & prev_rsi.sgt(&lower_neutrality)
                & back_2_rsi.sgt(&lower_neutrality)
                & back_3_rsi.sgt(&lower_neutrality),
            direction.seq(&MINUS_ONE)
                & prev_direction.seq(&MINUS_ONE)
                & back_2_direction.seq(&MINUS_ONE)
                & back_3_direction.seq(&MINUS_ONE)
                & rsi.slt(&NEUTRALITY_LINE)
                & rsi.sgt(&lower_barrier)
                & prev_rsi.slt(&upper_neutrality)
                & back_2_rsi.slt(&upper_neutrality)
                & back_3_rsi.slt(&upper_neutrality),
        )
    }
}
