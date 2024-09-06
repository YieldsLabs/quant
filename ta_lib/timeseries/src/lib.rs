mod model;
mod ohlcv;
mod ta;
mod traits;

pub mod prelude {
    pub use crate::model::BaseTimeSeries;
    pub use crate::ohlcv::{OHLCVSeries, OHLCV};
    pub use crate::ta::TechAnalysis;
    pub use crate::traits::*;
}

pub use prelude::*;
