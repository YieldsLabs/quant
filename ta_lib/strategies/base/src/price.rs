use crate::OHLCVSeries;
use core::prelude::*;
use price::prelude::*;
use volatility::atr;

pub trait Price {
    fn hl2(&self) -> Series<f32>;
    fn hlc3(&self) -> Series<f32>;
    fn hlcc4(&self) -> Series<f32>;
    fn ohlc4(&self) -> Series<f32>;
    fn atr(&self, period: usize) -> Series<f32>;
}

impl Price for OHLCVSeries {
    fn hl2(&self) -> Series<f32> {
        median_price(&self.high, &self.low)
    }

    fn hlc3(&self) -> Series<f32> {
        typical_price(&self.high, &self.low, &self.close)
    }

    fn hlcc4(&self) -> Series<f32> {
        wcl(&self.high, &self.low, &self.close)
    }

    fn ohlc4(&self) -> Series<f32> {
        average_price(&self.open, &self.high, &self.low, &self.close)
    }

    fn atr(&self, period: usize) -> Series<f32> {
        atr(&self.high, &self.low, &self.close, period, None)
    }
}
