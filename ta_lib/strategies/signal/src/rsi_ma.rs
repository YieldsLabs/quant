use base::{OHLCVSeries, Signal};
use core::Series;
use shared::{ma_indicator, rsi_indicator, MovingAverageType, RSIType};

pub struct RSIMASignal {
    rsi_type: RSIType,
    rsi_period: usize,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: MovingAverageType,
    smoothing_period: usize,
}

impl RSIMASignal {
    pub fn new(
        rsi_type: RSIType,
        rsi_period: f32,
        lower_barrier: f32,
        upper_barrier: f32,
        smoothing: MovingAverageType,
        smoothing_period: f32,
    ) -> Self {
        Self {
            rsi_type,
            rsi_period: rsi_period as usize,
            lower_barrier,
            upper_barrier,
            smoothing,
            smoothing_period: smoothing_period as usize,
        }
    }
}

impl Signal for RSIMASignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.rsi_period, self.smoothing_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.smoothing, data, self.smoothing_period);
        let rsi = rsi_indicator(&self.rsi_type, data, self.rsi_period);
        let close = Series::from(&data.close);

        let long_signal = ma.gt(&close) & rsi.slt(self.lower_barrier);
        let short_signal = ma.lt(&close) & rsi.sgt(self.upper_barrier);

        (long_signal, short_signal)
    }
}
