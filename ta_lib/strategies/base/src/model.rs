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
    pub open: Vec<f32>,
    pub high: Vec<f32>,
    pub low: Vec<f32>,
    pub close: Vec<f32>,
    pub volume: Vec<f32>,
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
            open,
            high,
            low,
            close,
            volume,
        }
    }
}
