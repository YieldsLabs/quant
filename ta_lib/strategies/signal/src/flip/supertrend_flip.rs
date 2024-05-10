use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use trend::supertrend;

pub struct SupertrendFlipSignal {
    source_type: SourceType,
    atr_period: usize,
    factor: f32,
}

impl SupertrendFlipSignal {
    pub fn new(source_type: SourceType, atr_period: f32, factor: f32) -> Self {
        Self {
            source_type,
            atr_period: atr_period as usize,
            factor,
        }
    }
}

impl Signal for SupertrendFlipSignal {
    fn lookback(&self) -> usize {
        self.atr_period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (direction, _) = supertrend(
            &data.source(self.source_type),
            data.close(),
            &data.atr(self.atr_period),
            self.factor,
        );

        (direction.cross_over(&ZERO), direction.cross_under(&ZERO))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_supertrend_flip_signal() {
        let signal = SupertrendFlipSignal::new(SourceType::HL2, 3.0, 3.0);
        let data = vec![
            OHLCV {
                ts: 1679827200,
                open: 6.161,
                high: 6.161,
                low: 6.136,
                close: 6.146,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679827500,
                open: 6.146,
                high: 6.150,
                low: 6.135,
                close: 6.148,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679827800,
                open: 6.148,
                high: 6.157,
                low: 6.143,
                close: 6.155,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828100,
                open: 6.155,
                high: 6.174,
                low: 6.155,
                close: 6.174,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828400,
                open: 6.174,
                high: 6.179,
                low: 6.163,
                close: 6.173,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828700,
                open: 6.173,
                high: 6.192,
                low: 6.170,
                close: 6.172,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829000,
                open: 6.172,
                high: 6.184,
                low: 6.167,
                close: 6.182,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829300,
                open: 6.182,
                high: 6.183,
                low: 6.170,
                close: 6.176,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829600,
                open: 6.176,
                high: 6.185,
                low: 6.161,
                close: 6.167,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829900,
                open: 6.167,
                high: 6.193,
                low: 6.165,
                close: 6.193,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679830200,
                open: 6.193,
                high: 6.213,
                low: 6.188,
                close: 6.201,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679830500,
                open: 6.201,
                high: 6.201,
                low: 6.183,
                close: 6.198,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679830800,
                open: 6.198,
                high: 6.205,
                low: 6.186,
                close: 6.188,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679831100,
                open: 6.188,
                high: 6.188,
                low: 6.168,
                close: 6.174,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679831400,
                open: 6.174,
                high: 6.180,
                low: 6.164,
                close: 6.176,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679831700,
                open: 6.176,
                high: 6.194,
                low: 6.176,
                close: 6.191,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679832000,
                open: 6.191,
                high: 6.191,
                low: 6.169,
                close: 6.175,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679832300,
                open: 6.175,
                high: 6.184,
                low: 6.175,
                close: 6.184,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679832600,
                open: 6.184,
                high: 6.194,
                low: 6.176,
                close: 6.188,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679832900,
                open: 6.188,
                high: 6.188,
                low: 6.171,
                close: 6.179,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679833200,
                open: 6.179,
                high: 6.188,
                low: 6.171,
                close: 6.184,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679833500,
                open: 6.184,
                high: 6.195,
                low: 6.182,
                close: 6.195,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679833800,
                open: 6.195,
                high: 6.212,
                low: 6.193,
                close: 6.210,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679834100,
                open: 6.210,
                high: 6.210,
                low: 6.180,
                close: 6.192,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679834400,
                open: 6.192,
                high: 6.193,
                low: 6.152,
                close: 6.173,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679834700,
                open: 6.173,
                high: 6.178,
                low: 6.161,
                close: 6.174,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679835000,
                open: 6.174,
                high: 6.189,
                low: 6.161,
                close: 6.189,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679835300,
                open: 6.189,
                high: 6.197,
                low: 6.183,
                close: 6.194,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679835600,
                open: 6.194,
                high: 6.205,
                low: 6.189,
                close: 6.202,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679835900,
                open: 6.202,
                high: 6.232,
                low: 6.193,
                close: 6.231,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679836200,
                open: 6.231,
                high: 6.236,
                low: 6.215,
                close: 6.218,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679836500,
                open: 6.218,
                high: 6.222,
                low: 6.205,
                close: 6.208,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679836800,
                open: 6.208,
                high: 6.233,
                low: 6.208,
                close: 6.224,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679837100,
                open: 6.224,
                high: 6.231,
                low: 6.213,
                close: 6.220,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679837400,
                open: 6.220,
                high: 6.224,
                low: 6.196,
                close: 6.208,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679837700,
                open: 6.208,
                high: 6.219,
                low: 6.202,
                close: 6.204,
                volume: 100.0,
            },
        ];

        let series = OHLCVSeries::from(data);

        let (long_signal, short_signal) = signal.generate(&series);

        let expected_long_signal = vec![
            false, false, false, false, false, false, false, false, false, false, false, false,
            false, false, false, false, false, false, false, false, false, false, true, false,
            false, false, false, false, false, false, false, false, false, false, false, false,
        ];
        let expected_short_signal = vec![
            false, false, false, false, false, false, false, false, false, false, false, false,
            false, false, false, false, false, false, false, false, false, false, false, false,
            false, false, false, false, false, false, false, false, false, false, false, false,
        ];

        let result_long_signal: Vec<bool> = long_signal.into();
        let result_short_signal: Vec<bool> = short_signal.into();

        assert_eq!(result_long_signal, expected_long_signal);
        assert_eq!(result_short_signal, expected_short_signal);
    }
}
