use crate::{OHLCVSeries, OHLCV};

pub trait TimeSeries: Send + Sync {
    fn add(&mut self, bar: &OHLCV);
    fn next_bar(&self, bar: &OHLCV) -> Option<OHLCV>;
    fn ohlcv(&self, size: usize) -> OHLCVSeries;
    fn len(&self) -> usize;
}
