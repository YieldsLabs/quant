use core::prelude::*;
use timeseries::prelude::*;
use volatility::{tr, wtr};

pub trait Volatility {
    fn atr(&self, smooth: Smooth, period: usize) -> Price;
    fn tr(&self) -> Price;
    fn wtr(&self) -> Price;
}

impl Volatility for OHLCVSeries {
    #[inline]
    fn atr(&self, smooth: Smooth, period: usize) -> Price {
        self.tr().smooth(smooth, period)
    }

    #[inline]
    fn tr(&self) -> Price {
        tr(self.high(), self.low(), self.close())
    }

    #[inline]
    fn wtr(&self) -> Price {
        wtr(self.high(), self.low(), self.close())
    }
}
