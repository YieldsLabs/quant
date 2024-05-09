mod ffi;
mod model;
mod ohlcv;

pub mod prelude {
    pub use crate::model::TimeSeries;
    pub use crate::ohlcv::{OHLCVSeries, OHLCV};
}

pub use ffi::*;
pub use prelude::*;
