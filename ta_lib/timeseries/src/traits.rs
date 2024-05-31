use crate::{OHLCVSeries, TechAnalysis, OHLCV};

pub trait TimeSeries: Send + Sync {
    fn add(&mut self, bar: &OHLCV);
    fn next_bar(&self, bar: &OHLCV) -> Option<OHLCV>;
    fn prev_bar(&self, bar: &OHLCV) -> Option<OHLCV>;
    fn ohlcv(&self, size: usize) -> OHLCVSeries;
    fn ta(&self, bar: &OHLCV) -> TechAnalysis;
    fn len(&self) -> usize;
}
