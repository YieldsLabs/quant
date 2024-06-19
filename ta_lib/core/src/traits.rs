pub trait Cross<T> {
    type Output;

    fn cross_over(&self, rhs: &T) -> Self::Output;
    fn cross_under(&self, rhs: &T) -> Self::Output;
    fn cross(&self, rhs: &T) -> Self::Output;
}

pub trait Extremum<T> {
    type Output;

    fn extremum<F>(&self, rhs: &T, f: F) -> Self::Output
    where
        F: Fn(f32, f32) -> f32;

    fn max(&self, rhs: &T) -> Self::Output;
    fn min(&self, rhs: &T) -> Self::Output;
    fn clip(&self, lhs: &T, rhs: &T) -> Self::Output;
}

pub trait Comparator<T> {
    type Output;

    fn compare<F>(&self, rhs: &T, comparator: F) -> Self::Output
    where
        F: Fn(f32, f32) -> bool;

    fn seq(&self, rhs: &T) -> Self::Output;
    fn sne(&self, rhs: &T) -> Self::Output;
    fn sgt(&self, rhs: &T) -> Self::Output;
    fn sgte(&self, rhs: &T) -> Self::Output;
    fn slt(&self, rhs: &T) -> Self::Output;
    fn slte(&self, rhs: &T) -> Self::Output;
}

pub trait Operation<T, U, V> {
    type Output;

    fn ops<F>(&self, rhs: &T, op: F) -> Self::Output
    where
        F: Fn(U, V) -> f32;

    fn sadd(&self, rhs: &T) -> Self::Output;
    fn ssub(&self, rhs: &T) -> Self::Output;
    fn smul(&self, rhs: &T) -> Self::Output;
    fn sdiv(&self, rhs: &T) -> Self::Output;
}

pub trait Bitwise<T> {
    type Output;

    fn op<F>(&self, rhs: &T, op: F) -> Self::Output
    where
        F: Fn(bool, bool) -> bool;

    fn sand(&self, rhs: &T) -> Self::Output;
    fn sor(&self, rhs: &T) -> Self::Output;
}
