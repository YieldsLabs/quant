use base::prelude::*;
use core::prelude::*;
use trend::vi;

pub struct ViConfirm {
    atr_period: usize,
    period: usize,
}

impl ViConfirm {
    pub fn new(atr_period: f32, period: f32) -> Self {
        Self {
            atr_period: atr_period as usize,
            period: period as usize,
        }
    }
}

impl Confirm for ViConfirm {
    fn lookback(&self) -> usize {
        std::cmp::max(self.atr_period, self.period)
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (vip, vim) = vi(
            data.high(),
            data.low(),
            &data.atr(self.atr_period, Smooth::SMMA),
            self.period,
        );

        (vip.sgt(&vim), vip.slt(&vim))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::VecDeque;

    #[test]
    fn test_confirm_vi() {
        let confirm = ViConfirm::new(1.0, 3.0);
        let data = VecDeque::from([
            OHLCV {
                ts: 1679827200,
                open: 6.490,
                high: 6.514,
                low: 6.490,
                close: 6.511,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679827500,
                open: 6.511,
                high: 6.522,
                low: 6.506,
                close: 6.512,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679827800,
                open: 6.512,
                high: 6.513,
                low: 6.496,
                close: 6.512,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828100,
                open: 6.512,
                high: 6.528,
                low: 6.507,
                close: 6.527,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828400,
                open: 6.527,
                high: 6.530,
                low: 6.497,
                close: 6.500,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828700,
                open: 6.500,
                high: 6.508,
                low: 6.489,
                close: 6.505,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829000,
                open: 6.505,
                high: 6.510,
                low: 6.483,
                close: 6.492,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829300,
                open: 6.492,
                high: 6.496,
                low: 6.481,
                close: 6.491,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829600,
                open: 6.491,
                high: 6.512,
                low: 6.486,
                close: 6.499,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829900,
                open: 6.499,
                high: 6.500,
                low: 6.481,
                close: 6.486,
                volume: 100.0,
            },
        ]);
        let series = OHLCVSeries::from_data(&data);

        let (long_signal, short_signal) = confirm.validate(&series);

        let expected_long_signal = vec![
            false, true, true, true, false, false, false, false, true, false,
        ];
        let expected_short_signal = vec![
            false, false, false, false, true, true, true, true, false, true,
        ];

        let result_long_signal: Vec<bool> = long_signal.into();
        let result_short_signal: Vec<bool> = short_signal.into();

        assert_eq!(result_long_signal, expected_long_signal);
        assert_eq!(result_short_signal, expected_short_signal);
    }
}
