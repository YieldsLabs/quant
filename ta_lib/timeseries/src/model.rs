use crate::{OHLCVSeries, TechAnalysis, TimeSeries, OHLCV};
use core::prelude::*;
use momentum::{cci, dmi, macd, roc, rsi, stochosc};
use price::{typical_price, wcl};
use std::collections::BTreeMap;
use trend::spp;
use volatility::{bb, gkyz, kch, tr, yz};
use volume::{mfi, nvol, obv, vwap};

#[derive(Debug, Clone)]
pub struct BaseTimeSeries {
    data: BTreeMap<i64, OHLCV>,
}

impl Default for BaseTimeSeries {
    fn default() -> Self {
        Self::new()
    }
}

impl BaseTimeSeries {
    pub fn new() -> Self {
        Self {
            data: BTreeMap::new(),
        }
    }
}

impl TimeSeries for BaseTimeSeries {
    fn add(&mut self, bar: &OHLCV) {
        self.data.insert(bar.ts, *bar);
    }

    fn next_bar(&self, bar: &OHLCV) -> Option<OHLCV> {
        self.data.range(bar.ts..).nth(1).map(|(_, &v)| v)
    }

    fn prev_bar(&self, bar: &OHLCV) -> Option<OHLCV> {
        self.data.range(..bar.ts).next_back().map(|(_, &v)| v)
    }

    fn back_n_bars(&self, bar: &OHLCV, n: usize) -> Vec<OHLCV> {
        self.data
            .range(..bar.ts)
            .rev()
            .take(n)
            .map(|(_, &v)| v)
            .collect()
    }

    #[inline]
    fn len(&self) -> usize {
        self.data.len()
    }

    fn ohlcv(&self, size: usize) -> OHLCVSeries {
        let len = self.len();
        let start_index = if len >= size { len - size } else { 0 };

        OHLCVSeries::from(
            self.data
                .range(..)
                .skip(start_index)
                .map(|(_, &v)| v)
                .collect::<Vec<_>>(),
        )
    }

    fn ta(&self, bar: &OHLCV) -> TechAnalysis {
        let periods = [2, 14, 12, 26, 9, 5, 10, 1, 3, 11];
        let factors = [1.8, 0.015, 1.0];

        let end_index = self
            .data
            .keys()
            .position(|&ts| ts >= bar.ts)
            .unwrap_or_else(|| self.len());
        let max_period = periods.iter().max().unwrap_or(&0);

        let start_index = if end_index > *max_period {
            end_index - max_period
        } else {
            0
        };

        let series = OHLCVSeries::from(
            self.data
                .values()
                .skip(start_index)
                .take(end_index - start_index)
                .copied()
                .collect::<Vec<_>>(),
        );

        let open = series.open();
        let high = series.high();
        let low = series.low();
        let source = series.close();
        let volume = series.volume();
        let hlc3 = typical_price(high, low, source);
        let hlcc4 = wcl(high, low, source);

        let rsi2 = rsi(source, Smooth::SMMA, periods[0]);
        let rsi14 = rsi(source, Smooth::SMMA, periods[1]);
        let ema5 = source.smooth(Smooth::EMA, periods[5]);
        let ema11 = source.smooth(Smooth::EMA, periods[9]);

        let (_, _, histogram) = macd(source, Smooth::EMA, periods[2], periods[3], periods[4]);
        let ppo = source.spread_pct(Smooth::EMA, periods[2], periods[3]);
        let vo = volume.spread_pct(Smooth::EMA, periods[5], periods[6]);
        let nvol = nvol(volume, Smooth::SMA, periods[4]);
        let obv = obv(source, volume);
        let mfi = mfi(&hlc3, volume, periods[1]);
        let tr = tr(high, low, source);
        let atr = tr.smooth(Smooth::SMMA, periods[1]);
        let gkyz = gkyz(open, high, low, source, periods[3]);
        let yz = yz(open, high, low, source, periods[3]);
        let (upb, _, lwb) = bb(source, Smooth::SMA, periods[5], factors[0]);
        let (upkch, _, lwkch) = kch(
            source,
            Smooth::SMA,
            &gkyz.smooth(Smooth::SMA, periods[1]),
            periods[5],
            factors[2],
        );
        let ebb = &upb - &lwb;
        let ekch = &upkch - &lwkch;
        let (k, d) = stochosc(
            source,
            high,
            low,
            Smooth::SMA,
            periods[1],
            periods[7],
            periods[8],
        );
        let cci = cci(&hlc3, periods[5], factors[1]);
        let roc9 = roc(source, periods[4]);
        let roc14 = roc(source, periods[1]);
        let hh = high.highest(periods[5]);
        let ll = low.lowest(periods[5]);
        let (support, resistance) = spp(high, low, source, Smooth::SMA, periods[2]);

        let (dp, dm, _) = dmi(high, low, &atr, Smooth::SMMA, periods[1], periods[1]);

        let dmi = dp - dm;
        let vwap = vwap(&hlc3, volume);

        TechAnalysis {
            frsi: rsi2.into(),
            srsi: rsi14.into(),
            fma: ema5.into(),
            sma: ema11.into(),
            froc: roc9.into(),
            sroc: roc14.into(),
            macd: histogram.into(),
            ppo: ppo.into(),
            cci: cci.into(),
            obv: obv.into(),
            vo: vo.into(),
            nvol: nvol.into(),
            mfi: mfi.into(),
            tr: tr.into(),
            gkyz: gkyz.into(),
            yz: yz.into(),
            upb: upb.into(),
            lwb: lwb.into(),
            ebb: ebb.into(),
            ekch: ekch.into(),
            k: k.into(),
            d: d.into(),
            hh: hh.into(),
            ll: ll.into(),
            support: support.into(),
            resistance: resistance.into(),
            dmi: dmi.into(),
            vwap: vwap.into(),
            close: source.clone().into(),
            hlc3: hlc3.into(),
            hlcc4: hlcc4.into(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_remove_dublicate() {
        let data = vec![
            OHLCV {
                ts: 1679826900,
                open: 5.992,
                high: 5.993,
                low: 5.976,
                close: 5.980,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679825700,
                open: 5.993,
                high: 6.000,
                low: 5.983,
                close: 5.997,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679826000,
                open: 5.997,
                high: 6.001,
                low: 5.989,
                close: 6.001,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679826000,
                open: 6.001,
                high: 6.0013,
                low: 5.993,
                close: 6.007,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679826600,
                open: 6.007,
                high: 6.008,
                low: 5.980,
                close: 5.992,
                volume: 100.0,
            },
        ];
        let mut ts = BaseTimeSeries::new();

        for bar in &data {
            ts.add(bar);
        }

        assert_eq!(ts.len(), data.len() - 1)
    }

    #[test]
    fn test_right_order() {
        let data = vec![
            OHLCV {
                ts: 1679825700,
                open: 5.993,
                high: 6.000,
                low: 5.983,
                close: 5.997,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679826000,
                open: 5.997,
                high: 6.001,
                low: 5.989,
                close: 6.001,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679826600,
                open: 6.007,
                high: 6.008,
                low: 5.980,
                close: 5.992,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679826300,
                open: 6.001,
                high: 6.0013,
                low: 5.993,
                close: 6.007,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679826900,
                open: 5.992,
                high: 5.993,
                low: 5.976,
                close: 5.980,
                volume: 100.0,
            },
        ];
        let mut ts = BaseTimeSeries::new();

        for bar in &data {
            ts.add(bar);
        }

        let curr_bar = OHLCV {
            ts: 1679826000,
            open: 5.997,
            high: 6.001,
            low: 5.989,
            close: 6.001,
            volume: 100.0,
        };

        let next_bar = OHLCV {
            ts: 1679826300,
            open: 6.001,
            high: 6.0013,
            low: 5.993,
            close: 6.007,
            volume: 100.0,
        };

        let prev_bar = OHLCV {
            ts: 1679825700,
            open: 5.993,
            high: 6.000,
            low: 5.983,
            close: 5.997,
            volume: 100.0,
        };
        let n = 2;

        let back_bars = ts.back_n_bars(&curr_bar, n);

        assert_eq!(ts.next_bar(&curr_bar).unwrap(), next_bar);
        assert_eq!(ts.prev_bar(&curr_bar).unwrap(), prev_bar);
        assert_eq!(back_bars.len(), 1);
        assert_eq!(back_bars[0], prev_bar);
    }

    #[test]
    fn test_ohlcv() {
        let data = vec![
            OHLCV {
                ts: 1679825700,
                open: 5.993,
                high: 6.000,
                low: 5.983,
                close: 5.997,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679826000,
                open: 5.997,
                high: 6.001,
                low: 5.989,
                close: 6.001,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679826300,
                open: 6.001,
                high: 6.0013,
                low: 5.993,
                close: 6.007,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679826600,
                open: 6.007,
                high: 6.008,
                low: 5.980,
                close: 5.992,
                volume: 100.0,
            },
            OHLCV {
                ts: 1679826900,
                open: 5.992,
                high: 5.993,
                low: 5.976,
                close: 5.980,
                volume: 100.0,
            },
        ];
        let mut ts = BaseTimeSeries::new();

        for bar in &data {
            ts.add(bar);
        }

        let series = ts.ohlcv(3);
        let close: Vec<f32> = series.close().clone().into();

        assert_eq!(series.len(), 3);
        assert_eq!(close[0], 6.007);
        assert_eq!(close[1], 5.992);
        assert_eq!(close[2], 5.980);
    }
}
