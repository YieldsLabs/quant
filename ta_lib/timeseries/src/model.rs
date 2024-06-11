use crate::{OHLCVSeries, TechAnalysis, TimeSeries, OHLCV};
use core::prelude::*;
use momentum::{cci, macd, ppo, roc, rsi, stochosc};
use price::typical_price;
use std::collections::HashMap;
use trend::spp;
use volatility::{bbp, gkyz, tr, yz};
use volume::{mfi, nvol, obv, vo};

const BUFF_FACTOR: f32 = 1.3;

#[derive(Debug, Clone)]
pub struct BaseTimeSeries {
    index: HashMap<i64, usize>,
    data: Vec<OHLCV>,
}

impl Default for BaseTimeSeries {
    fn default() -> Self {
        Self::new()
    }
}

impl BaseTimeSeries {
    const CAPACITY: usize = 600000;

    pub fn new() -> Self {
        Self {
            index: HashMap::with_capacity(Self::CAPACITY),
            data: Vec::with_capacity(Self::CAPACITY),
        }
    }

    fn shift_up(&mut self, mut index: usize) {
        while index > 0 {
            let parent_index = index - 1;

            if self.data[parent_index].ts <= self.data[index].ts {
                break;
            }

            self.data.swap(index, parent_index);
            self.index.insert(self.data[index].ts, index);
            self.index.insert(self.data[parent_index].ts, parent_index);
            index = parent_index;
        }

        self.index.insert(self.data[index].ts, index);
    }
}

impl TimeSeries for BaseTimeSeries {
    fn add(&mut self, bar: &OHLCV) {
        if let Some(&existing_idx) = self.index.get(&bar.ts) {
            self.data[existing_idx] = *bar;
        } else {
            let idx = self.len();
            self.index.insert(bar.ts, idx);
            self.data.push(*bar);
            self.shift_up(idx);
        }
    }

    fn next_bar(&self, bar: &OHLCV) -> Option<OHLCV> {
        self.index
            .get(&bar.ts)
            .and_then(|&idx| self.data.get(idx + 1).copied())
    }

    fn prev_bar(&self, bar: &OHLCV) -> Option<OHLCV> {
        self.index
            .get(&bar.ts)
            .and_then(|&idx| self.data.get(idx - 1).copied())
    }

    #[inline]
    fn len(&self) -> usize {
        self.index.len()
    }

    fn ohlcv(&self, size: usize) -> OHLCVSeries {
        let buff_size = (size as f32 * BUFF_FACTOR) as usize;

        let start_index = if self.len() >= buff_size {
            self.len() - buff_size
        } else {
            0
        };

        OHLCVSeries::from(&self.data[start_index..])
    }

    fn ta(&self, bar: &OHLCV) -> TechAnalysis {
        let periods = [2, 14, 12, 26, 9, 5, 10, 1, 3, 11];
        let factors = [1.8, 0.015];

        let end_index = *self.index.get(&bar.ts).unwrap_or(&self.data.len());
        let max_period = periods.into_iter().max().unwrap_or(0);

        let start_index = if end_index > max_period {
            end_index - max_period
        } else {
            0
        };

        let series = OHLCVSeries::from(&self.data[start_index..end_index]);

        let open = series.open();
        let high = series.high();
        let low = series.low();
        let source = series.close();
        let volume = series.volume();
        let hlc3 = typical_price(high, low, source);

        let rsi2 = rsi(source, Smooth::SMMA, periods[0]);
        let rsi14 = rsi(source, Smooth::SMMA, periods[1]);
        let ema5 = source.smooth(Smooth::EMA, periods[5]);
        let ema11 = source.smooth(Smooth::EMA, periods[9]);

        let (_, _, histogram) = macd(source, Smooth::EMA, periods[2], periods[3], periods[4]);
        let ppo = ppo(source, Smooth::EMA, periods[2], periods[3]);
        let vo = vo(volume, Smooth::EMA, periods[5], periods[6]);
        let nvol = nvol(volume, Smooth::SMA, periods[4]);
        let obv = obv(source, volume);
        let mfi = mfi(&hlc3, volume, periods[1]);
        let tr = tr(high, low, source);
        let gkyz = gkyz(open, high, low, source, periods[3]);
        let yz = yz(open, high, low, source, periods[3]);
        let bbp = bbp(source, Smooth::SMA, periods[5], factors[0]);
        let (k, d) = stochosc(
            source,
            high,
            low,
            Smooth::SMA,
            periods[1],
            periods[7],
            periods[8],
        );
        let cci = cci(&hlc3, Smooth::SMA, periods[5], factors[1]);
        let roc9 = roc(source, periods[4]);
        let roc14 = roc(source, periods[1]);
        let hh = high.highest(periods[5]);
        let ll = low.lowest(periods[5]);
        let (support, resistance) = spp(high, low, source, Smooth::SMA, periods[2]);

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
            bbp: bbp.into(),
            k: k.into(),
            d: d.into(),
            hh: hh.into(),
            ll: ll.into(),
            support: support.into(),
            resistance: resistance.into(),
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

        assert_eq!(ts.next_bar(&curr_bar).unwrap(), next_bar);
        assert_eq!(ts.prev_bar(&curr_bar).unwrap(), prev_bar);
    }
}
