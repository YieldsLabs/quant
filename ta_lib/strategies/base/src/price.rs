use crate::OHLCVSeries;
use core::prelude::*;
use price::prelude::*;
use volatility::{atr, tr};

pub trait Price {
    fn hl2(&self) -> Series<f32>;
    fn hlc3(&self) -> Series<f32>;
    fn hlcc4(&self) -> Series<f32>;
    fn ohlc4(&self) -> Series<f32>;
    fn atr(&self, period: usize, smooth_type: Smooth) -> Series<f32>;
    fn tr(&self) -> Series<f32>;
}

impl Price for OHLCVSeries {
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

    #[inline]
    fn atr(&self, period: usize, smooth_type: Smooth) -> Series<f32> {
        atr(&self.high, &self.low, &self.close, smooth_type, period)
    }

    #[inline]
    fn tr(&self) -> Series<f32> {
        tr(&self.high, &self.low, &self.close)
    }
}
