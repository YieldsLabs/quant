use core::prelude::*;
use timeseries::prelude::*;
use volatility::{atr, tr};

pub trait Volatility {
    fn atr(&self, period: usize) -> Series<f32>;
    fn tr(&self) -> Series<f32>;
}

impl Volatility for OHLCVSeries {
    #[inline]
    fn atr(&self, period: usize) -> Series<f32> {
        atr(self.high(), self.low(), self.close(), Smooth::SMMA, period)
    }

    #[inline]
    fn tr(&self) -> Series<f32> {
        tr(self.high(), self.low(), self.close())
    }
}
