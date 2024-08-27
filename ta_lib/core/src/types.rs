use crate::series::Series;

pub type Scalar = f32;
pub type Price = Series<Scalar>;
pub type Rule = Series<bool>;
pub type Period = usize;
