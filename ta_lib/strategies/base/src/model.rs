use core::prelude::*;
use std::collections::VecDeque;

#[derive(Debug, Copy, Clone)]
pub struct OHLCV {
    pub open: f32,
    pub high: f32,
    pub low: f32,
    pub close: f32,
    pub volume: f32,
}

#[derive(Debug, Clone)]
pub struct OHLCVSeries {
    pub open: Series<f32>,
    pub high: Series<f32>,
    pub low: Series<f32>,
    pub close: Series<f32>,
    pub volume: Series<f32>,
}

impl OHLCVSeries {
    pub fn from_data(data: &VecDeque<OHLCV>) -> Self {
        let len = data.len();

        let mut open = Vec::with_capacity(len);
        let mut high = Vec::with_capacity(len);
        let mut low = Vec::with_capacity(len);
        let mut close = Vec::with_capacity(len);
        let mut volume = Vec::with_capacity(len);

        for ohlcv in data.iter() {
            open.push(ohlcv.open);
            high.push(ohlcv.high);
            low.push(ohlcv.low);
            close.push(ohlcv.close);
            volume.push(ohlcv.volume);
        }

        Self {
            open: Series::from(open),
            high: Series::from(high),
            low: Series::from(low),
            close: Series::from(close),
            volume: Series::from(volume),
        }
    }
}
