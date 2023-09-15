use base::{BaseStrategy, OHLCVSeries, Signals};
use core::series::Series;
use stop_loss::ATRStopLoss;
use trend::{
    alma, dema, ema, frama, gma, hma, kama, rmsma, sinwma, sma, smma, t3, tema, tma, vwma, wma,
    zlema,
};

pub struct CrossMAStrategy<'a> {
    short_period: usize,
    long_period: usize,
    smothing: &'a str,
}

impl CrossMAStrategy<'_> {
    pub fn new(
        smothing: &str,
        short_period: usize,
        long_period: usize,
        atr_period: usize,
        stop_loss_multi: f32,
    ) -> BaseStrategy<CrossMAStrategy, ATRStopLoss> {
        let lookback_period = std::cmp::max(short_period, long_period);
        let signal = CrossMAStrategy {
            short_period,
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

impl Signals for CrossMAStrategy<'_> {
    fn id(&self) -> String {
        format!(
            "CROSS_{}:{}:{}",
            self.smothing, self.short_period, self.long_period
        )
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let short_ma = self.ma(data, self.short_period);
        let long_ma = self.ma(data, self.long_period);

        let long_signal = short_ma.cross_over(&long_ma);
        let short_signal = short_ma.cross_under(&long_ma);

        (long_signal, short_signal)
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use base::{Strategy, TradeAction, OHLCV};

    #[test]
    fn test_crossmatrategy_new() {
        let strategy = CrossMAStrategy::new("SMA", 50, 100, 14, 2.0);
        assert_eq!(strategy.id(), "_STRTGCROSS_SMA:50:100_STPLSSATR_14:2.0");
    }

    #[test]
    fn test_crossmastrategy_next_do_nothing() {
        let mut strat = CrossMAStrategy::new("SMA", 50, 100, 14, 2.0);

        for _i in 0..100 {
            strat.next(OHLCV {
                open: 2.0,
                high: 3.0,
                low: 2.0,
                close: 3.0,
                volume: 2000.0,
            });
        }

        let result = strat.next(OHLCV {
            open: 1.0,
            high: 1.0,
            low: 1.0,
            close: 1.0,
            volume: 20.0,
        });

        assert_eq!(result, TradeAction::DoNothing);
    }
}
