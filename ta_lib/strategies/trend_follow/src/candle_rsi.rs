use base::{BaseStrategy, OHLCVSeries, Signals};
use core::series::Series;
use momentum::rsi;
use shared::trend_candle;
use stop_loss::ATRStopLoss;

pub struct CandleRSIStrategy<'a> {
    candle: &'a str,
    rsi_period: usize,
}

impl CandleRSIStrategy<'_> {
    pub fn new<'a>(
        candle: &'a str,
        rsi_period: usize,
        atr_period: usize,
        stop_loss_multi: f32,
    ) -> BaseStrategy<CandleRSIStrategy<'_>, ATRStopLoss> {
        let lookback_period = std::cmp::max(rsi_period, atr_period);
        let signal = CandleRSIStrategy { candle, rsi_period };

        let stop_loss = ATRStopLoss {
            atr_period,
            multi: stop_loss_multi,
        };

        BaseStrategy::new(signal, stop_loss, lookback_period)
    }
}

impl Signals for CandleRSIStrategy<'_> {
    fn id(&self) -> String {
        format!("CANDLERSI_{}:{}", self.candle, self.rsi_period)
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (bullish_candle, bearish_candle) = trend_candle(self.candle, data);
        let rsi = rsi(&data.close, self.rsi_period);

        let long_signal = bullish_candle & rsi.sgt(50.0);
        let short_signal = bearish_candle & rsi.slt(50.0);

        (long_signal, short_signal)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
