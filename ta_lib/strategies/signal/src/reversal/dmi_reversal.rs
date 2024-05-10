use base::prelude::*;
use core::prelude::*;
use momentum::dmi;
use timeseries::prelude::*;

pub struct DmiReversalSignal {
    smooth_type: Smooth,
    adx_period: usize,
    di_period: usize,
}

impl DmiReversalSignal {
    pub fn new(smooth_type: Smooth, adx_period: f32, di_period: f32) -> Self {
        Self {
            smooth_type,
            adx_period: adx_period as usize,
            di_period: di_period as usize,
        }
    }
}

impl Signal for DmiReversalSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.adx_period, self.di_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (_, di_plus, di_minus) = dmi(
            data.high(),
            data.low(),
            &data.atr(self.di_period),
            self.smooth_type,
            self.adx_period,
            self.di_period,
        );
        (
            di_plus.cross_over(&di_minus),
            di_plus.cross_under(&di_minus),
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_signal_dmi_reversal() {
        let signal = DmiReversalSignal::new(Smooth::SMMA, 3.0, 3.0);
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

        let (dip, dim) = signal.generate(&series);

        let expected_long_signal = vec![false, false, false, false, false, false, false, false];
        let expected_short_signal = vec![false, false, false, false, false, true, false, false];

        let result_long_signal: Vec<bool> = dip.into();
        let result_short_signal: Vec<bool> = dim.into();

        assert_eq!(result_long_signal, expected_long_signal);
        assert_eq!(result_short_signal, expected_short_signal);
    }
}
