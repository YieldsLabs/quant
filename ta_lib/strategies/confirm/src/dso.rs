use base::prelude::*;
use core::prelude::*;
use momentum::dso;

pub struct DsoConfirm {
    smooth_type: Smooth,
    smooth_period: usize,
    k_period: usize,
    d_period: usize,
}

impl DsoConfirm {
    pub fn new(smooth_type: Smooth, smooth_period: f32, k_period: f32, d_period: f32) -> Self {
        Self {
            smooth_type,
            smooth_period: smooth_period as usize,
            k_period: k_period as usize,
            d_period: d_period as usize,
        }
    }
}

impl Confirm for DsoConfirm {
    fn lookback(&self) -> usize {
        let period = std::cmp::max(self.smooth_period, self.k_period);
        std::cmp::max(period, self.d_period)
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (k, d) = dso(
            &data.close,
            self.smooth_type,
            self.smooth_period,
            self.k_period,
            self.d_period,
        );

        (k.sgt(&d), k.slt(&d))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use core::prelude::*;
    use std::collections::VecDeque;

    #[test]
    fn test_confirm_dso() {
        let confirm = DsoConfirm::new(Smooth::EMA, 13.0, 8.0, 9.0);
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

        let (long_signal, short_signal) = confirm.validate(&series);

        let expected_long_signal = vec![
            false, true, true, true, true, true, true, true, true, true, false, false, false,
            false, false,
        ];
        let expected_short_signal = vec![
            false, false, false, false, false, false, false, false, false, false, true, true, true,
            true, true,
        ];

        let result_long_signal: Vec<bool> = long_signal.into();
        let result_short_signal: Vec<bool> = short_signal.into();

        assert_eq!(result_long_signal, expected_long_signal);
        assert_eq!(expected_short_signal, result_short_signal);
    }
}
