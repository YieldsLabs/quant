use base::prelude::*;
use core::prelude::*;
use momentum::dmi;
use timeseries::prelude::*;

pub struct Dmi2LinesCrossSignal {
    smooth: Smooth,
    period_adx: usize,
    period_di: usize,
}

impl Dmi2LinesCrossSignal {
    pub fn new(smooth: Smooth, period_adx: f32, period_di: f32) -> Self {
        Self {
            smooth,
            period_adx: period_adx as usize,
            period_di: period_di as usize,
        }
    }
}

impl Signal for Dmi2LinesCrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period_adx, self.period_di)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (dip, dim, _) = dmi(
            data.high(),
            data.low(),
            &data.atr(self.smooth, self.period_di),
            self.smooth,
            self.period_adx,
            self.period_di,
        );

        (dip.cross_over(&dim), dip.cross_under(&dim))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_signal_dmi_cross() {
        let signal = Dmi2LinesCrossSignal::new(Smooth::SMMA, 3.0, 3.0);
        let data = vec![
            OHLCV {
                ts: 1679827200,
                open: 0.010631,
                high: 0.010655,
                low: 0.010612,
                close: 0.010651,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679827500,
                open: 0.010651,
                high: 0.010671,
                low: 0.010596,
                close: 0.010665,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679827800,
                open: 0.010665,
                high: 0.010720,
                low: 0.010661,
                close: 0.010693,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828100,
                open: 0.010693,
                high: 0.010711,
                low: 0.010651,
                close: 0.010698,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828400,
                open: 0.010698,
                high: 0.010761,
                low: 0.010675,
                close: 0.010688,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828700,
                open: 0.010688,
                high: 0.010688,
                low: 0.010614,
                close: 0.010625,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829000,
                open: 0.010625,
                high: 0.010629,
                low: 0.010533,
                close: 0.010548,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829300,
                open: 0.010548,
                high: 0.010563,
                low: 0.010501,
                close: 0.010515,
                volume: 100.0,
            },
        ];
        let series = OHLCVSeries::from(data);

        let (dip, dim) = signal.trigger(&series);

        let expected_long_signal = vec![false, false, false, false, false, false, false, false];
        let expected_short_signal = vec![false, false, false, false, false, true, false, false];

        let result_long_signal: Vec<bool> = dip.into();
        let result_short_signal: Vec<bool> = dim.into();

        assert_eq!(result_long_signal, expected_long_signal);
        assert_eq!(result_short_signal, expected_short_signal);
    }
}
