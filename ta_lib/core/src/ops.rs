use crate::constants::ZERO;
use crate::series::Series;
use crate::traits::Operation;
use std::ops::{Add, Div, Mul, Sub};

impl Operation<f32, f32, f32> for Series<f32> {
    type Output = Series<f32>;

    fn ops<F>(&self, scalar: &f32, op: F) -> Self::Output
    where
        F: Fn(f32, f32) -> f32,
    {
        self.fmap(|val| val.map(|v| op(*v, *scalar)))
    }

    fn sadd(&self, scalar: &f32) -> Self::Output {
        self.ops(scalar, |v, s| v + s)
    }

    fn smul(&self, scalar: &f32) -> Self::Output {
        self.ops(scalar, |v, s| v * s)
    }

    fn sdiv(&self, scalar: &f32) -> Self::Output {
        self.ops(scalar, |v, s| if s != ZERO { v / s } else { ZERO })
    }

    fn ssub(&self, scalar: &f32) -> Self::Output {
        self.ops(scalar, |v, s| v - s)
    }
}

impl Operation<Series<f32>, f32, f32> for Series<f32> {
    type Output = Series<f32>;

    fn ops<F>(&self, rhs: &Series<f32>, op: F) -> Self::Output
    where
        F: Fn(f32, f32) -> f32,
    {
        self.zip_with(rhs, |a, b| {
            a.and_then(|a_val| b.map(|b_val| op(*a_val, *b_val)))
        })
    }

    fn sadd(&self, rhs: &Series<f32>) -> Self::Output {
        self.ops(rhs, |v, s| v + s)
    }

    fn smul(&self, rhs: &Series<f32>) -> Self::Output {
        self.ops(rhs, |v, s| v * s)
    }

    fn sdiv(&self, rhs: &Series<f32>) -> Self::Output {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(_a_val), Some(b_val)) if *b_val == ZERO => Some(ZERO),
            (Some(a_val), Some(b_val)) if *b_val != ZERO => Some(a_val / b_val),
            _ => None,
        })
    }

    fn ssub(&self, rhs: &Series<f32>) -> Self::Output {
        self.ops(rhs, |v, s| v - s)
    }
}

impl Operation<Series<f32>, bool, f32> for Series<bool> {
    type Output = Series<f32>;

    fn ops<F>(&self, rhs: &Series<f32>, op: F) -> Self::Output
    where
        F: Fn(bool, f32) -> f32,
    {
        self.zip_with(rhs, |b, a| match (b, a) {
            (Some(b_val), Some(a_val)) => Some(op(*b_val, *a_val)),
            _ => None,
        })
    }

    fn sadd(&self, _rhs: &Series<f32>) -> Self::Output {
        unimplemented!()
    }

    fn smul(&self, rhs: &Series<f32>) -> Self::Output {
        self.ops(rhs, |b, a| if b { a } else { ZERO })
    }

    fn sdiv(&self, _rhs: &Series<f32>) -> Self::Output {
        unimplemented!()
    }

    fn ssub(&self, _rhs: &Series<f32>) -> Self::Output {
        unimplemented!()
    }
}

macro_rules! impl_series_ops {
    ($trait_name:ident, $trait_method:ident, $method:ident) => {
        impl $trait_name<Series<f32>> for &Series<f32> {
            type Output = Series<f32>;

            fn $trait_method(self, rhs: Series<f32>) -> Self::Output {
                self.$method(&rhs)
            }
        }

        impl $trait_name<&Series<f32>> for Series<f32> {
            type Output = Series<f32>;

            fn $trait_method(self, rhs: &Series<f32>) -> Self::Output {
                self.$method(rhs)
            }
        }

        impl $trait_name<&Series<f32>> for &Series<f32> {
            type Output = Series<f32>;

            fn $trait_method(self, rhs: &Series<f32>) -> Self::Output {
                self.$method(rhs)
            }
        }

        impl $trait_name<Series<f32>> for Series<f32> {
            type Output = Series<f32>;

            fn $trait_method(self, rhs: Series<f32>) -> Self::Output {
                self.$method(&rhs)
            }
        }
    };
}

impl_series_ops!(Add, add, sadd);
impl_series_ops!(Mul, mul, smul);
impl_series_ops!(Div, div, sdiv);
impl_series_ops!(Sub, sub, ssub);

macro_rules! impl_scalar_ops {
    ($trait_name:ident, $trait_method:ident, $method:ident) => {
        impl $trait_name<&Series<f32>> for f32 {
            type Output = Series<f32>;

            fn $trait_method(self, rhs: &Series<f32>) -> Self::Output {
                rhs.$method(&self)
            }
        }

        impl $trait_name<Series<f32>> for f32 {
            type Output = Series<f32>;

            fn $trait_method(self, rhs: Series<f32>) -> Self::Output {
                rhs.$method(&self)
            }
        }

        impl $trait_name<f32> for &Series<f32> {
            type Output = Series<f32>;

            fn $trait_method(self, scalar: f32) -> Self::Output {
                self.$method(&scalar)
            }
        }

        impl $trait_name<f32> for Series<f32> {
            type Output = Series<f32>;

            fn $trait_method(self, scalar: f32) -> Self::Output {
                self.$method(&scalar)
            }
        }
    };
}

impl_scalar_ops!(Add, add, sadd);
impl_scalar_ops!(Mul, mul, smul);

impl Div<f32> for &Series<f32> {
    type Output = Series<f32>;

    fn div(self, scalar: f32) -> Self::Output {
        self.sdiv(&scalar)
    }
}

impl Div<f32> for Series<f32> {
    type Output = Series<f32>;

    fn div(self, scalar: f32) -> Self::Output {
        self.sdiv(&scalar)
    }
}

impl Div<&Series<f32>> for f32 {
    type Output = Series<f32>;

    fn div(self, rhs: &Series<f32>) -> Self::Output {
        Series::fill(self, rhs.len()).sdiv(rhs)
    }
}

impl Div<Series<f32>> for f32 {
    type Output = Series<f32>;

    fn div(self, rhs: Series<f32>) -> Self::Output {
        Series::fill(self, rhs.len()).sdiv(&rhs)
    }
}

impl Sub<f32> for &Series<f32> {
    type Output = Series<f32>;

    fn sub(self, scalar: f32) -> Self::Output {
        self.ssub(&scalar)
    }
}

impl Sub<f32> for Series<f32> {
    type Output = Series<f32>;

    fn sub(self, scalar: f32) -> Self::Output {
        self.ssub(&scalar)
    }
}

impl Sub<&Series<f32>> for f32 {
    type Output = Series<f32>;

    fn sub(self, rhs: &Series<f32>) -> Self::Output {
        rhs.negate().ssub(&-self)
    }
}

impl Sub<Series<f32>> for f32 {
    type Output = Series<f32>;

    fn sub(self, rhs: Series<f32>) -> Self::Output {
        rhs.negate().ssub(&-self)
    }
}

macro_rules! impl_bool_ops {
    ($trait_name:ident, $trait_method:ident, $method:ident) => {
        impl $trait_name<&Series<f32>> for &Series<bool> {
            type Output = Series<f32>;

            fn $trait_method(self, rhs: &Series<f32>) -> Self::Output {
                self.$method(rhs)
            }
        }

        impl $trait_name<&Series<f32>> for Series<bool> {
            type Output = Series<f32>;

            fn $trait_method(self, rhs: &Series<f32>) -> Self::Output {
                self.$method(rhs)
            }
        }
    };
}

impl_bool_ops!(Mul, mul, smul);
