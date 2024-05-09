use core::prelude::*;
use serde::Deserialize;

#[derive(Debug, Copy, Clone, PartialEq, Deserialize)]
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
}

impl<'a> From<&'a [OHLCV]> for OHLCVSeries {
    fn from(data: &'a [OHLCV]) -> Self {
        Self {
            open: Series::from(data.iter().map(|bar| bar.open).collect::<Vec<_>>()),
            high: Series::from(data.iter().map(|bar| bar.high).collect::<Vec<_>>()),
            low: Series::from(data.iter().map(|bar| bar.low).collect::<Vec<_>>()),
            close: Series::from(data.iter().map(|bar| bar.close).collect::<Vec<_>>()),
            volume: Series::from(data.iter().map(|bar| bar.volume).collect::<Vec<_>>()),
        }
    }
}

impl From<Vec<OHLCV>> for OHLCVSeries {
    fn from(data: Vec<OHLCV>) -> Self {
        OHLCVSeries::from(&data[..])
    }
}
