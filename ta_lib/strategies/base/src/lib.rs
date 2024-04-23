extern crate alloc;

mod constants;
mod ffi;
mod model;
mod source;
mod strategy;
mod traits;
mod volatility;

pub mod prelude {
    pub use crate::constants::*;
    pub use crate::ffi::*;
    pub use crate::model::{OHLCVSeries, OHLCV};
    pub use crate::source::*;
    pub use crate::strategy::{BaseStrategy, StopLossLevels, TradeAction};
    pub use crate::traits::*;
    pub use crate::volatility::*;
}

pub use prelude::*;
