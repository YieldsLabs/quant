use crate::OHLCVSeries;
use core::prelude::*;
use volatility::{atr, tr};

pub trait Volatility {
    fn atr(&self, period: usize, smooth_type: Smooth) -> Series<f32>;
    fn tr(&self) -> Series<f32>;
}

impl Volatility for OHLCVSeries {
    #[inline]
    fn atr(&self, period: usize, smooth_type: Smooth) -> Series<f32> {
        atr(&self.high, &self.low, &self.close, smooth_type, period)
    }

    #[inline]
    fn tr(&self) -> Series<f32> {
        tr(&self.high, &self.low, &self.close)
    }
}
