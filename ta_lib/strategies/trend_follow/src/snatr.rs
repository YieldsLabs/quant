use base::{BaseStrategy, OHLCVSeries, Signals};
use core::series::Series;
use shared::ma;
use stop_loss::ATRStopLoss;
use volatility::atr;

pub struct SNATRStrategy<'a> {
    atr_period: usize,
    atr_smoothing_period: usize,
    long_period: usize,
    smoothing: &'a str,
}

impl SNATRStrategy<'_> {
    pub fn new(
        atr_period: usize,
        atr_smoothing_period: usize,
        smoothing: &str,
        long_period: usize,
        stop_loss_atr_period: usize,
        stop_loss_multi: f32,
    ) -> BaseStrategy<SNATRStrategy, ATRStopLoss> {
        let lookback_period = std::cmp::max(atr_period, long_period);
        let signal = SNATRStrategy {
            atr_period,
            atr_smoothing_period,
            long_period,
            smoothing,
        };

        let stop_loss = ATRStopLoss {
            atr_period: stop_loss_atr_period,
            multi: stop_loss_multi,
        };

        BaseStrategy::new(signal, stop_loss, lookback_period)
    }
}

impl Signals for SNATRStrategy<'_> {
    fn id(&self) -> String {
        format!(
            "SNATR_{}:{}:{}:{}",
            self.atr_period, self.atr_smoothing_period, self.smoothing, self.long_period
        )
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let atr = atr(&data.high, &data.low, &data.close, self.atr_period, None);
        let snatr = (&atr - &atr.lowest(self.atr_period))
            / (&atr.highest(self.atr_period) - &atr.lowest(self.atr_period))
                .wma(self.atr_smoothing_period);
        let ma = ma(self.smoothing, data, self.long_period);
        let close = Series::from(&data.close);

        let long_signal = snatr.slt(0.8) & snatr.shift(1).sgt(0.8) & close.gt(&ma);
        let short_signal = snatr.sgt(0.2) & snatr.shift(1).slt(0.2) & close.lt(&ma);

        (long_signal, short_signal)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
