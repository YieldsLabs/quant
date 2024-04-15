use base::prelude::*;
use core::prelude::*;
use trend::vi;

pub struct ViReversalSignal {
    atr_period: usize,
    period: usize,
}

impl ViReversalSignal {
    pub fn new(atr_period: f32, period: f32) -> Self {
        Self {
            atr_period: atr_period as usize,
            period: period as usize,
        }
    }
}

impl Signal for ViReversalSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.atr_period, self.period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (vip, vim) = vi(
            &data.high,
            &data.low,
            &data.atr(self.atr_period, Smooth::SMMA),
            self.period,
        );

        (vip.cross_over(&vim), vip.cross_under(&vim))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use core::prelude::*;
    use std::collections::VecDeque;

    #[test]
    fn test_signal_vi_reversal() {
        let signal = ViReversalSignal::new(1.0, 2.0);
        let data = VecDeque::from([
            OHLCV {
                open: 4.8914,
                high: 4.9045,
                low: 4.8895,
                close: 4.8995,
                volume: 100.0,
            },
            OHLCV {
                open: 4.8995,
                high: 4.9073,
                low: 4.8995,
                close: 4.9061,
                volume: 100.0,
            },
            OHLCV {
                open: 4.9061,
                high: 4.9070,
                low: 4.9001,
                close: 4.9001,
                volume: 100.0,
            },
            OHLCV {
                open: 4.9001,
                high: 4.9053,
                low: 4.8995,
                close: 4.9053,
                volume: 100.0,
            },
            OHLCV {
                open: 4.9053,
                high: 4.9093,
                low: 4.9046,
                close: 4.9087,
                volume: 100.0,
            },
            OHLCV {
                open: 4.9087,
                high: 4.9154,
                low: 4.9087,
                close: 4.9131,
                volume: 100.0,
            },
            OHLCV {
                open: 4.9131,
                high: 4.9131,
                low: 4.9040,
                close: 4.9041,
                volume: 100.0,
            },
            OHLCV {
                open: 4.9041,
                high: 4.9068,
                low: 4.8988,
                close: 4.9023,
                volume: 100.0,
            },
            OHLCV {
                open: 4.9023,
                high: 4.9051,
                low: 4.8949,
                close: 4.9010,
                volume: 100.0,
            },
            OHLCV {
                open: 4.9010,
                high: 4.9052,
                low: 4.8969,
                close: 4.8969,
                volume: 100.0,
            },
            OHLCV {
                open: 4.8969,
                high: 4.8969,
                low: 4.8819,
                close: 4.8895,
                volume: 100.0,
            },
            OHLCV {
                open: 4.8895,
                high: 4.8928,
                low: 4.8851,
                close: 4.8901,
                volume: 100.0,
            },
            OHLCV {
                open: 4.8901,
                high: 4.8910,
                low: 4.8813,
                close: 4.8855,
                volume: 100.0,
            },
            OHLCV {
                open: 4.8855,
                high: 4.8864,
                low: 4.8816,
                close: 4.8824,
                volume: 100.0,
            },
            OHLCV {
                open: 4.8824,
                high: 4.8934,
                low: 4.8814,
                close: 4.8925,
                volume: 100.0,
            },
        ]);
        let series = OHLCVSeries::from_data(&data);

        let (vip, vim) = signal.generate(&series);

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
