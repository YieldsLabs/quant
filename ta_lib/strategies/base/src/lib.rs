extern crate alloc;

mod ffi;
mod source;
mod strategy;
mod traits;
mod volatility;

pub mod prelude {
    pub use crate::ffi::*;
    pub use crate::source::*;
    pub use crate::strategy::{BaseStrategy, StopLossLevels, TradeAction};
    pub use crate::traits::*;
    pub use crate::volatility::*;
}

pub use prelude::*;
