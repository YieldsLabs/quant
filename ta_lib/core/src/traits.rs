pub trait Cross<T> {
    type Output;

    fn cross_over(&self, rhs: T) -> Self::Output;
    fn cross_under(&self, rhs: T) -> Self::Output;
    fn cross(&self, rhs: T) -> Self::Output;
}

pub trait Extremum<T> {
    type Output;

    fn max(&self, rhs: T) -> Self::Output;
    fn min(&self, rhs: T) -> Self::Output;
}
