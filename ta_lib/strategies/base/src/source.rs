use core::prelude::*;
use price::prelude::*;
use timeseries::prelude::*;

#[derive(Copy, Clone)]
pub enum SourceType {
    CLOSE,
    HL2,
    HLC3,
    HLCC4,
    OHLC4,
}

pub trait Source {
    fn source(&self, source_type: SourceType) -> Series<f32>;
}

impl Source for OHLCVSeries {
    #[inline]
    fn source(&self, source_type: SourceType) -> Series<f32> {
        match source_type {
            SourceType::CLOSE => self.close().clone(),
            SourceType::HL2 => median_price(self.high(), self.low()),
            SourceType::HLC3 => typical_price(self.high(), self.low(), self.close()),
            SourceType::HLCC4 => wcl(self.high(), self.low(), self.close()),
            SourceType::OHLC4 => average_price(self.open(), self.high(), self.low(), self.close()),
        }
    }
}
