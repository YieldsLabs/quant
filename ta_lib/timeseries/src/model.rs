use crate::{OHLCVSeries, OHLCV};
use core::prelude::*;
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct TimeSeries {
    index: HashMap<i64, usize>,
    pub data: Vec<OHLCV>,
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
            index: HashMap::new(),
            data: Vec::with_capacity(Self::CAPACITY),
        }
    }

    pub fn add(&mut self, bar: OHLCV) {
        if let Some(&existing_idx) = self.index.get(&bar.ts) {
            self.data[existing_idx] = bar;
            self._sift_up(existing_idx);
        } else {
            let idx = self.data.len();

            self.index.insert(bar.ts, idx);
            self.data.push(bar);
            self._sift_up(idx);
        }
    }

    fn _sift_up(&mut self, index: usize) {
        let mut index = index;

        while index > 0 {
            let parent_index = (index - 1) / 2;

            if self.data[index].ts < self.data[parent_index].ts {
                self.data.swap(index, parent_index);
                self.index.insert(self.data[index].ts, index);
                self.index.insert(self.data[parent_index].ts, parent_index);
                index = parent_index;
            } else {
                break;
            }
        }
    }

    pub fn next_bar(&self, bar: &OHLCV) -> Option<&OHLCV> {
        self.index
            .get(&bar.ts)
            .and_then(|&idx| self.data.get(idx + 1))
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
