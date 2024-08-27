use crate::series::Series;

pub type Price = Series<f32>;
pub type Rule = Series<bool>;
pub type Period = usize;
pub type Scalar = f32;
