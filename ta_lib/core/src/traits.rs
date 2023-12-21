pub trait Cross<T> {
    type Output;

    fn cross_over(&self, rhs: &T) -> Self::Output;
    fn cross_under(&self, rhs: &T) -> Self::Output;
    fn cross(&self, rhs: &T) -> Self::Output;
}

pub trait Extremum<T> {
    type Output;

    fn max(&self, rhs: &T) -> Self::Output;
    fn min(&self, rhs: &T) -> Self::Output;
}

pub trait Comparator<T> {
    type Output;

    fn compare<F>(&self, rhs: &T, comparator: F) -> Self::Output
    where
        F: Fn(f32, f32) -> bool;

    fn seq(&self, rhs: &T) -> Self::Output;
    fn sne(&self, rhs: &T) -> Self::Output;
    fn sgt(&self, rhs: &T) -> Self::Output;
    fn sge(&self, rhs: &T) -> Self::Output;
    fn slt(&self, rhs: &T) -> Self::Output;
    fn sle(&self, rhs: &T) -> Self::Output;
}
