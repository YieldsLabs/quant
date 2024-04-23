use crate::OHLCVSeries;
use core::prelude::*;
use price::prelude::*;

pub trait Source {
    fn hl2(&self) -> Series<f32>;
    fn hlc3(&self) -> Series<f32>;
    fn hlcc4(&self) -> Series<f32>;
    fn ohlc4(&self) -> Series<f32>;
}

impl Source for OHLCVSeries {
    #[inline]
    fn hl2(&self) -> Series<f32> {
        median_price(&self.high, &self.low)
    }

    #[inline]
    fn hlc3(&self) -> Series<f32> {
        typical_price(&self.high, &self.low, &self.close)
    }

    #[inline]
    fn hlcc4(&self) -> Series<f32> {
        wcl(&self.high, &self.low, &self.close)
    }

    #[inline]
    fn ohlc4(&self) -> Series<f32> {
        average_price(&self.open, &self.high, &self.low, &self.close)
    }
}
