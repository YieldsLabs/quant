use base::prelude::*;
use channel::a;
use core::prelude::*;
use timeseries::prelude::*;
use volatility::kch;

pub struct KchASignal {
    source: SourceType,
    smooth: Smooth,
    period: usize,
    smooth_atr: Smooth,
    period_atr: usize,
    factor: f32,
}

impl KchASignal {
    pub fn new(
        source: SourceType,
        smooth: Smooth,
        period: f32,
        smooth_atr: Smooth,
        period_atr: f32,
        factor: f32,
    ) -> Self {
        Self {
            source,
            smooth,
            period: period as usize,
            smooth_atr,
            period_atr: period_atr as usize,
            factor,
        }
    }
}

impl Signal for KchASignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.period_atr)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let source = data.source(self.source);
        let atr = data.atr(self.smooth_atr, self.period_atr);
        let (upper, _, lower) = kch(&source, self.smooth, &atr, self.period, self.factor);

        a!(source, upper, lower)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kch_a_ults_signal() {
        let signal = KchASignal::new(SourceType::HLC3, Smooth::ULTS, 5.0, Smooth::ULTS, 5.0, 0.3);
        let data = vec![
            OHLCV {
                ts: 1679827200,
                open: 0.29437,
                high: 0.29606,
                low: 0.29415,
                close: 0.29456,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679827500,
                open: 0.29456,
                high: 0.29623,
                low: 0.29456,
                close: 0.29603,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679827800,
                open: 0.29603,
                high: 0.29620,
                low: 0.29263,
                close: 0.29263,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828100,
                open: 0.29263,
                high: 0.29329,
                low: 0.28850,
                close: 0.28877,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828400,
                open: 0.28877,
                high: 0.29104,
                low: 0.28599,
                close: 0.29085,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679828700,
                open: 0.29085,
                high: 0.29393,
                low: 0.29085,
                close: 0.29241,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829000,
                open: 0.29241,
                high: 0.29318,
                low: 0.29202,
                close: 0.29287,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829300,
                open: 0.29287,
                high: 0.29355,
                low: 0.29223,
                close: 0.29304,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829600,
                open: 0.29304,
                high: 0.29305,
                low: 0.29130,
                close: 0.29153,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679829900,
                open: 0.29153,
                high: 0.29216,
                low: 0.28969,
                close: 0.28991,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679830200,
                open: 0.28991,
                high: 0.29068,
                low: 0.28866,
                close: 0.28879,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679830500,
                open: 0.28879,
                high: 0.28941,
                low: 0.28830,
                close: 0.28860,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679830800,
                open: 0.28860,
                high: 0.29012,
                low: 0.28837,
                close: 0.28940,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679831100,
                open: 0.28940,
                high: 0.29074,
                low: 0.28940,
                close: 0.29074,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679831400,
                open: 0.29074,
                high: 0.29270,
                low: 0.29074,
                close: 0.29270,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679831700,
                open: 0.29270,
                high: 0.29419,
                low: 0.29270,
                close: 0.29390,
                volume: 100.0,
            },
        ];

        let series = OHLCVSeries::from(data);

        let (long_signal, short_signal) = signal.trigger(&series);

        let expected_long_signal = vec![
            false, false, false, false, true, false, false, false, false, true, false, false,
            false, false, false, false,
        ];
        let expected_short_signal = vec![
            false, false, false, false, false, false, true, false, false, false, false, false,
            false, false, true, false,
        ];

        let result_long_signal: Vec<bool> = long_signal.into();
        let result_short_signal: Vec<bool> = short_signal.into();

        assert_eq!(result_long_signal, expected_long_signal);
        assert_eq!(result_short_signal, expected_short_signal);
    }
}
