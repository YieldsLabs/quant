use base::{BaseStrategy, OHLCVSeries, Signals};
use core::series::Series;
use shared::{ma, trend_candle};
use stop_loss::ATRStopLoss;

pub struct CandleMAStrategy<'a, 'b> {
    candle: &'a str,
    smoothing: &'b str,
    long_period: usize,
}

impl CandleMAStrategy<'_, '_> {
    pub fn new<'a, 'b>(
        candle: &'a str,
        smoothing: &'b str,
        long_period: usize,
        atr_period: usize,
        stop_loss_multi: f32,
    ) -> BaseStrategy<CandleMAStrategy<'a, 'b>, ATRStopLoss> {
        let lookback_period = long_period;
        let signal = CandleMAStrategy {
            candle,
            smoothing,
            long_period,
        };

        let stop_loss = ATRStopLoss {
            atr_period,
            multi: stop_loss_multi,
        };

        BaseStrategy::new(signal, stop_loss, lookback_period)
    }
}

impl Signals for CandleMAStrategy<'_, '_> {
    fn id(&self) -> String {
        format!(
            "CANDLEMA_{}:{}:{}",
            self.candle, self.smoothing, self.long_period
        )
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma(self.smoothing, data, self.long_period);
        let (bullish_candle, bearish_candle) = trend_candle(self.candle, data);
        let close = Series::from(&data.close);

        let long_signal = bullish_candle & close.gt(&ma);
        let short_signal = bearish_candle & close.lt(&ma);

        (long_signal, short_signal)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
