use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use volatility::yz;

pub struct YzPulse {
    period: usize,
    smooth_signal: Smooth,
    period_signal: usize,
}

impl YzPulse {
    pub fn new(period: f32, smooth_signal: Smooth, period_signal: f32) -> Self {
        Self {
            period: period as usize,
            smooth_signal,
            period_signal: period_signal as usize,
        }
    }
}

impl Pulse for YzPulse {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.period_signal)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let yz = yz(
            data.open(),
            data.high(),
            data.low(),
            data.close(),
            self.period,
        );
        let signal = yz.smooth(self.smooth_signal, self.period_signal);

        (yz.sgt(&signal), yz.sgt(&signal))
    }
}
