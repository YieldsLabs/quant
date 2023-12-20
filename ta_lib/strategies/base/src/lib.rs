extern crate alloc;

mod ffi;
mod model;
mod price;
mod strategy;
mod traits;

pub mod prelude {
    pub use crate::ffi::*;
    pub use crate::model::{OHLCVSeries, OHLCV};
    pub use crate::price::*;
    pub use crate::strategy::{BaseStrategy, StopLossLevels, TradeAction};
    pub use crate::traits::*;
}

pub use prelude::*;
