use crate::OHLCVSeries;
use price::{average::average_price, median::median_price, typical::typical_price, wcl::wcl};

pub trait Price {
    fn hl2(&self) -> Vec<f32>;
    fn hlc3(&self) -> Vec<f32>;
    fn hlcc4(&self) -> Vec<f32>;
    fn ohlc4(&self) -> Vec<f32>;
}

impl Price for OHLCVSeries {
    fn hl2(&self) -> Vec<f32> {
        median_price(&self.high, &self.low)
    }
    fn hlc3(&self) -> Vec<f32> {
        typical_price(&self.high, &self.low, &self.close)
    }
    fn hlcc4(&self) -> Vec<f32> {
        wcl(&self.high, &self.low, &self.close)
    }
    fn ohlc4(&self) -> Vec<f32> {
        average_price(&self.open, &self.high, &self.low, &self.close)
    }
}
