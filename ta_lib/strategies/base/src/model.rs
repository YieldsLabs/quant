use core::prelude::*;
use std::collections::{HashSet, VecDeque};

#[derive(Debug, Copy, Clone)]
pub struct OHLCV {
    pub ts: i64,
    pub open: f32,
    pub high: f32,
    pub low: f32,
    pub close: f32,
    pub volume: f32,
}

#[derive(Debug, Clone)]
pub struct OHLCVSeries {
    open: Series<f32>,
    high: Series<f32>,
    low: Series<f32>,
    close: Series<f32>,
    volume: Series<f32>,
}

impl OHLCVSeries {
    pub fn from_data(data: &VecDeque<OHLCV>) -> Self {
        let len = data.len();

        let mut open = Vec::with_capacity(len);
        let mut high = Vec::with_capacity(len);
        let mut low = Vec::with_capacity(len);
        let mut close = Vec::with_capacity(len);
        let mut volume = Vec::with_capacity(len);

        let mut visited = HashSet::new();

        let mut sorted_data: Vec<_> = data.iter().collect();
        sorted_data.sort_by_key(|v| v.ts);

        for ohlcv in sorted_data.iter() {
            if !visited.contains(&ohlcv.ts) {
                open.push(ohlcv.open);
                high.push(ohlcv.high);
                low.push(ohlcv.low);
                close.push(ohlcv.close);
                volume.push(ohlcv.volume);

                visited.insert(ohlcv.ts);
            }
        }

        Self {
            open: Series::from(open),
            high: Series::from(high),
            low: Series::from(low),
            close: Series::from(close),
            volume: Series::from(volume),
        }
    }

    #[inline]
    pub fn len(&self) -> usize {
        self.close.len()
    }

    #[inline]
    pub fn open(&self) -> &Series<f32> {
        &self.open
    }

    #[inline]
    pub fn high(&self) -> &Series<f32> {
        &self.high
    }

    #[inline]
    pub fn low(&self) -> &Series<f32> {
        &self.low
    }

    #[inline]
    pub fn close(&self) -> &Series<f32> {
        &self.close
    }

    #[inline]
    pub fn volume(&self) -> &Series<f32> {
        &self.volume
    }
}
