use crate::{OHLCVSeries, OHLCV};
use core::prelude::*;
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct TimeSeries {
    index: HashMap<i64, usize>,
    data: Vec<OHLCV>,
}

impl Default for TimeSeries {
    fn default() -> Self {
        Self::new()
    }
}

impl TimeSeries {
    const CAPACITY: usize = 600000;

    pub fn new() -> Self {
        Self {
            index: HashMap::with_capacity(Self::CAPACITY),
            data: Vec::with_capacity(Self::CAPACITY),
        }
    }

    pub fn add(&mut self, bar: &OHLCV) {
        if let Some(&existing_idx) = self.index.get(&bar.ts) {
            self.data[existing_idx] = *bar;
        } else {
            let idx = self.data.len();
            self.index.insert(bar.ts, idx);
            self.data.push(*bar);
            self._shift_up(idx);
        }
    }

    fn _shift_up(&mut self, mut index: usize) {
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

    pub fn next_bar(&self, bar: &OHLCV) -> Option<OHLCV> {
        self.index
            .get(&bar.ts)
            .and_then(|&idx| self.data.get(idx + 1).copied())
    }

    #[inline]
    pub fn len(&self) -> usize {
        self.index.len()
    }

    pub fn ohlcv(&self, size: usize) -> OHLCVSeries {
        let start_index = if self.data.len() >= size {
            self.data.len() - size
        } else {
            0
        };

        OHLCVSeries::from(&self.data[start_index..])
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
        let mut ts = TimeSeries::new();

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
        let mut ts = TimeSeries::new();

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

        assert_eq!(ts.next_bar(&curr_bar).unwrap(), next_bar);
    }
}