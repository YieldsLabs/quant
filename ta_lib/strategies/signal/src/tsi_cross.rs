use base::{OHLCVSeries, Signal};
use core::{Cross, Series};
use momentum::tsi;

pub struct TSICrossSignal {
    long_period: usize,
    short_period: usize,
    signal_period: usize,
}

impl TSICrossSignal {
    pub fn new(long_period: f32, short_period: f32, signal_period: f32) -> Self {
        Self {
            long_period: long_period as usize,
            short_period: short_period as usize,
            signal_period: signal_period as usize,
        }
    }
}

impl Signal for TSICrossSignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.short_period, self.long_period);
        std::cmp::max(adj_lookback, self.signal_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tsi = tsi(&data.close, self.long_period, self.short_period);
        let signal_line = tsi.ema(self.signal_period);

        (tsi.cross_over(&signal_line), tsi.cross_under(&signal_line))
    }
}
