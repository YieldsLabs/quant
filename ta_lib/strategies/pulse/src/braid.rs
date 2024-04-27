use base::prelude::*;
use core::prelude::*;

pub struct BraidPulse {
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
    open_period: usize,
    strength: f32,
    atr_period: usize,
}

impl BraidPulse {
    pub fn new(
        smooth_type: Smooth,
        fast_period: f32,
        slow_period: f32,
        open_period: f32,
        strength: f32,
        atr_period: f32,
    ) -> Self {
        Self {
            smooth_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
            open_period: open_period as usize,
            strength,
            atr_period: atr_period as usize,
        }
    }
}

impl Pulse for BraidPulse {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.open_period)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let fast_ma = data.close.smooth(self.smooth_type, self.fast_period);
        let open_ma = data.open.smooth(self.smooth_type, self.open_period);
        let slow_ma = data.close.smooth(self.smooth_type, self.slow_period);

        let filter = data.atr(self.atr_period, Smooth::SMMA) * self.strength / 100.0;

        let max = fast_ma.max(&open_ma).max(&slow_ma);
        let min = fast_ma.min(&open_ma).min(&slow_ma);

        let histogram = max - min;

        (
            histogram.sgt(&filter)
                & (fast_ma.cross_over(&open_ma)
                    | (histogram.cross_over(&filter) & fast_ma.sgt(&open_ma))),
            histogram.sgt(&filter)
                & (fast_ma.cross_under(&open_ma)
                    | (histogram.cross_over(&filter) & fast_ma.slt(&open_ma))),
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::VecDeque;

    #[test]
    fn test_pulse_braid() {
        let pulse = BraidPulse::new(Smooth::LSMA, 3.0, 14.0, 7.0, 40.0, 14.0);
        let data = VecDeque::from([
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
                ts: 1679828100,
                open: 4.9053,
                high: 4.9093,
                low: 4.9046,
                close: 4.9087,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828400,
                open: 4.9087,
                high: 4.9154,
                low: 4.9087,
                close: 4.9131,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828700,
                open: 4.9131,
                high: 4.9131,
                low: 4.9040,
                close: 4.9041,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829000,
                open: 4.9041,
                high: 4.9068,
                low: 4.8988,
                close: 4.9023,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829300,
                open: 4.9023,
                high: 4.9051,
                low: 4.8949,
                close: 4.9010,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829600,
                open: 4.9010,
                high: 4.9052,
                low: 4.8969,
                close: 4.8969,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829900,
                open: 4.8969,
                high: 4.8969,
                low: 4.8819,
                close: 4.8895,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679830200,
                open: 4.8895,
                high: 4.8928,
                low: 4.8851,
                close: 4.8901,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679830500,
                open: 4.8901,
                high: 4.8910,
                low: 4.8813,
                close: 4.8855,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679830800,
                open: 4.8855,
                high: 4.8864,
                low: 4.8816,
                close: 4.8824,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679831100,
                open: 4.8824,
                high: 4.8934,
                low: 4.8814,
                close: 4.8925,
                volume: 100.0,
            },
        ]);
        let series = OHLCVSeries::from_data(&data);

        let (long_signal, short_signal) = pulse.assess(&series);

        let expected_long_signal = vec![
            false, false, false, false, false, false, false, false, false, false, false, false,
            false, false, true,
        ];
        let expected_short_signal = vec![
            false, false, false, false, false, false, true, false, false, false, false, false,
            false, false, false,
        ];

        let result_long_signal: Vec<bool> = long_signal.into();
        let result_short_signal: Vec<bool> = short_signal.into();

        assert_eq!(result_long_signal, expected_long_signal);
        assert_eq!(result_short_signal, expected_short_signal);
    }
}
