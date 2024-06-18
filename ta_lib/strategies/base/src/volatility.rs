use core::prelude::*;
use timeseries::prelude::*;
use volatility::tr;

pub trait Volatility {
    fn atr(&self, smooth: Smooth, period: usize) -> Series<f32>;
    fn tr(&self) -> Series<f32>;
}

impl Volatility for OHLCVSeries {
    #[inline]
    fn atr(&self, smooth: Smooth, period: usize) -> Series<f32> {
        self.tr().smooth(smooth, period)
    }

    #[inline]
    fn tr(&self) -> Series<f32> {
        tr(self.high(), self.low(), self.close())
    }
}
