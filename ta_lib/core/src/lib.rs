mod bitwise;
mod cmp;
mod constants;
mod cross;
mod extremum;
mod fmt;
mod from;
mod macros;
mod math;
mod ops;
mod series;
mod smoothing;
mod traits;
mod types;

pub mod prelude {
    pub use crate::constants::*;
    pub use crate::series::Series;
    pub use crate::smoothing::Smooth;
    pub use crate::traits::*;
    pub use crate::types::*;
    pub use crate::{iff, nz};
}

pub use prelude::*;
