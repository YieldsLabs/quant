use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use trend::vi;

pub struct Vi2LinesCrossSignal {
    period: usize,
    smooth_atr: Smooth,
    period_atr: usize,
}

impl Vi2LinesCrossSignal {
    pub fn new(period: f32, smooth_atr: Smooth, period_atr: f32) -> Self {
        Self {
            period: period as usize,
            smooth_atr,
            period_atr: period_atr as usize,
        }
    }
}

impl Signal for Vi2LinesCrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period_atr, self.period)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (vip, vim) = vi(
            data.high(),
            data.low(),
            &data.atr(self.smooth_atr, self.period_atr),
            self.period,
        );

        (vip.cross_over(&vim), vip.cross_under(&vim))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_signal_vi_cross() {
        let signal = Vi2LinesCrossSignal::new(2.0, Smooth::SMMA, 1.0);
        let data = vec![
            OHLCV {
                ts: 1679827200,
                open: 4.8914,
                high: 4.9045,
                low: 4.8895,
                close: 4.8995,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679827500,
                open: 4.8995,
                high: 4.9073,
                low: 4.8995,
                close: 4.9061,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679827800,
                open: 4.9061,
                high: 4.9070,
                low: 4.9001,
                close: 4.9001,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828100,
                open: 4.9001,
                high: 4.9053,
                low: 4.8995,
                close: 4.9053,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828400,
                open: 4.9053,
                high: 4.9093,
                low: 4.9046,
                close: 4.9087,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828700,
                open: 4.9087,
                high: 4.9154,
                low: 4.9087,
                close: 4.9131,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829000,
                open: 4.9131,
                high: 4.9131,
                low: 4.9040,
                close: 4.9041,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829300,
                open: 4.9041,
                high: 4.9068,
                low: 4.8988,
                close: 4.9023,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829600,
                open: 4.9023,
                high: 4.9051,
                low: 4.8949,
                close: 4.9010,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829900,
                open: 4.9010,
                high: 4.9052,
                low: 4.8969,
                close: 4.8969,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679830200,
                open: 4.8969,
                high: 4.8969,
                low: 4.8819,
                close: 4.8895,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679830500,
                open: 4.8895,
                high: 4.8928,
                low: 4.8851,
                close: 4.8901,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679830800,
                open: 4.8901,
                high: 4.8910,
                low: 4.8813,
                close: 4.8855,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679831100,
                open: 4.8855,
                high: 4.8864,
                low: 4.8816,
                close: 4.8824,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679831400,
                open: 4.8824,
                high: 4.8934,
                low: 4.8814,
                close: 4.8925,
                volume: 100.0,
            },
        ];
        let series = OHLCVSeries::from(data);

        let (vip, vim) = signal.trigger(&series);

        let expected_long_signal = vec![
            false, false, false, false, true, false, false, false, false, false, false, false,
            false, false, true,
        ];
        let expected_short_signal = vec![
            false, false, false, true, false, false, false, true, false, false, false, false,
            false, false, false,
        ];

        let result_long_signal: Vec<bool> = vip.into();
        let result_short_signal: Vec<bool> = vim.into();

        assert_eq!(result_long_signal, expected_long_signal);
        assert_eq!(result_short_signal, expected_short_signal);
    }
}
