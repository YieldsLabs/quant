use base::{BaseStrategy, OHLCVSeries, Signals};
use core::series::Series;
use stop_loss::ATRStopLoss;
use trend::{
    alma, dema, ema, frama, gma, hma, kama, rmsma, sinwma, sma, smma, t3, tema, tma, vwma, wma,
    zlema,
};

pub struct TestingGroundStrategy<'a> {
    long_period: usize,
    smothing: &'a str,
}

impl TestingGroundStrategy<'_> {
    pub fn new(
        smothing: &str,
        long_period: usize,
        atr_period: usize,
        stop_loss_multi: f32,
    ) -> BaseStrategy<TestingGroundStrategy, ATRStopLoss> {
        let lookback_period = long_period;
        let signal = TestingGroundStrategy {
            long_period,
            smothing,
        };

        let stop_loss = ATRStopLoss {
            atr_period,
            multi: stop_loss_multi,
        };

        BaseStrategy::new(signal, stop_loss, lookback_period)
    }

    fn ma(&self, data: &OHLCVSeries, period: usize) -> Series<f32> {
        match self.smothing {
            "ALMA" => alma(&data.close, period, 0.85, 6.0),
            "DEMA" => dema(&data.close, period),
            "EMA" => ema(&data.close, period),
            "FRAMA" => frama(&data.high, &data.low, &data.close, period),
            "GMA" => gma(&data.close, period),
            "HMA" => hma(&data.close, period),
            "KAMA" => kama(&data.close, period),
            "RMSMA" => rmsma(&data.close, period),
            "SINWMA" => sinwma(&data.close, period),
            "SMA" => sma(&data.close, period),
            "SMMA" => smma(&data.close, period),
            "T3" => t3(&data.close, period),
            "TEMA" => tema(&data.close, period),
            "TMA" => tma(&data.close, period),
            "VWMA" => vwma(&data.close, &data.volume, period),
            "WMA" => wma(&data.close, period),
            "ZLEMA" => zlema(&data.close, period),
            _ => sma(&data.close, period),
        }
    }
}

impl Signals for TestingGroundStrategy<'_> {
    fn id(&self) -> String {
        format!("GROUND_{}:{}", self.smothing, self.long_period)
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = self.ma(data, self.long_period);

        let open = Series::from(&data.open);
        let high = Series::from(&data.high);
        let low = Series::from(&data.low);
        let close = Series::from(&data.close);

        let long_signal = low.lt(&ma)
            & low.shift(1).lt(&ma.shift(1))
            & low.shift(2).lt(&ma.shift(2))
            & close.min(&open).gt(&ma)
            & close.shift(1).min(&open.shift(1)).gt(&ma.shift(1))
            & close.shift(2).min(&open.shift(2)).gt(&ma.shift(2));

        let short_signal = high.gt(&ma)
            & high.shift(1).gt(&ma.shift(1))
            & high.shift(2).gt(&ma.shift(2))
            & close.max(&open).lt(&ma)
            & close.shift(1).max(&open.shift(1)).lt(&ma.shift(1))
            & close.shift(2).max(&open.shift(2)).lt(&ma.shift(2));

        (long_signal, short_signal)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
