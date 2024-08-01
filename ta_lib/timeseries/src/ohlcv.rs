use core::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Debug, Copy, Clone, PartialEq, Serialize, Deserialize)]
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
    ts: Vec<i64>,
    open: Series<f32>,
    high: Series<f32>,
    low: Series<f32>,
    close: Series<f32>,
    volume: Series<f32>,
}

impl OHLCVSeries {
    pub fn open(&self) -> &Series<f32> {
        &self.open
    }

    pub fn high(&self) -> &Series<f32> {
        &self.high
    }

    pub fn low(&self) -> &Series<f32> {
        &self.low
    }

    pub fn close(&self) -> &Series<f32> {
        &self.close
    }

    pub fn volume(&self) -> &Series<f32> {
        &self.volume
    }

    pub fn len(&self) -> usize {
        self.close.len()
    }

    pub fn bar_index(&self, bar: &OHLCV) -> usize {
        self.ts
            .binary_search_by(|&ts| ts.cmp(&bar.ts))
            .unwrap_or_else(|_| self.len())
    }
}

impl<'a> From<&'a [OHLCV]> for OHLCVSeries {
    fn from(data: &'a [OHLCV]) -> Self {
        let len = data.len();

        let mut ts = Vec::with_capacity(len);
        let mut open = Vec::with_capacity(len);
        let mut high = Vec::with_capacity(len);
        let mut low = Vec::with_capacity(len);
        let mut close = Vec::with_capacity(len);
        let mut volume = Vec::with_capacity(len);

        for bar in data {
            ts.push(bar.ts);
            open.push(bar.open);
            high.push(bar.high);
            low.push(bar.low);
            close.push(bar.close);
            volume.push(bar.volume);
        }

        Self {
            ts,
            open: Series::from(open),
            high: Series::from(high),
            low: Series::from(low),
            close: Series::from(close),
            volume: Series::from(volume),
        }
    }
}

impl From<Vec<OHLCV>> for OHLCVSeries {
    fn from(data: Vec<OHLCV>) -> Self {
        OHLCVSeries::from(&data[..])
    }
}
