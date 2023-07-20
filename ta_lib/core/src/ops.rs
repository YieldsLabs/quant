use crate::series::Series;
use std::ops::{Add, Div, Mul, Neg, Sub};

impl Series<f64> {
    fn binary_op_series<F>(&self, rhs: &Series<f64>, op: F) -> Series<f64>
    where
        F: Fn(&f64, &f64) -> f64,
    {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(op(a_val, b_val)),
            _ => None,
        })
    }

    fn unary_op_scalar<F>(&self, scalar: f64, op: F) -> Series<f64>
    where
        F: Fn(&f64, f64) -> f64,
    {
        self.fmap(|val| val.map(|v| op(v, scalar)))
    }

    pub fn neg(&self) -> Series<f64> {
        self.fmap(|val| val.map(|v| v.neg()))
    }

    pub fn add_series(&self, rhs: &Series<f64>) -> Series<f64> {
        self.binary_op_series(rhs, |a, b| a + b)
    }

    pub fn mul_series(&self, rhs: &Series<f64>) -> Series<f64> {
        self.binary_op_series(rhs, |a, b| a * b)
    }

    pub fn div_series(&self, rhs: &Series<f64>) -> Series<f64> {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => {
                if *b_val == 0.0 {
                    if *a_val > 0.0 {
                        Some(std::f64::INFINITY)
                    } else if *a_val < 0.0 {
                        Some(std::f64::NEG_INFINITY)
                    } else {
                        None
                    }
                } else {
                    Some(a_val / b_val)
                }
            }
            _ => None,
        })
    }

    pub fn sub_series(&self, rhs: &Series<f64>) -> Series<f64> {
        self.binary_op_series(rhs, |a, b| a - b)
    }

    pub fn add_scalar(&self, scalar: f64) -> Series<f64> {
        self.unary_op_scalar(scalar, |v, s| v + s)
    }

    pub fn mul_scalar(&self, scalar: f64) -> Series<f64> {
        self.unary_op_scalar(scalar, |v, s| v * s)
    }

    pub fn div_scalar(&self, scalar: f64) -> Series<f64> {
        self.unary_op_scalar(scalar, |v, s| {
            if *v == 0.0 {
                if s > 0.0 {
                    std::f64::INFINITY
                } else if s < 0.0 {
                    std::f64::NEG_INFINITY
                } else {
                    0.0
                }
            } else {
                v / s
            }
        })
    }

    pub fn sub_scalar(&self, scalar: f64) -> Series<f64> {
        self.unary_op_scalar(scalar, |v, s| v - s)
    }
}

impl Neg for &Series<f64> {
    type Output = Series<f64>;

    fn neg(self) -> Series<f64> {
        self.neg()
    }
}

impl Series<bool> {
    fn bool_op_series<F>(&self, rhs: &Series<f64>, op: F) -> Series<f64>
    where
        F: Fn(&bool, &f64) -> f64,
    {
        self.zip_with(rhs, |b, a| match (b, a) {
            (Some(b_val), Some(a_val)) => Some(op(b_val, a_val)),
            _ => None,
        })
    }

    pub fn mul_series(&self, rhs: &Series<f64>) -> Series<f64> {
        self.bool_op_series(rhs, |b, a| if *b { *a } else { 0.0 })
    }
}

macro_rules! impl_series_ops {
    ($trait_name:ident, $trait_method:ident, $method:ident) => {
        impl $trait_name<Series<f64>> for &Series<f64> {
            type Output = Series<f64>;
            fn $trait_method(self, rhs: Series<f64>) -> Series<f64> {
                self.$method(&rhs)
            }
        }

        impl $trait_name<&Series<f64>> for Series<f64> {
            type Output = Series<f64>;
            fn $trait_method(self, rhs: &Series<f64>) -> Series<f64> {
                self.$method(rhs)
            }
        }

        impl $trait_name<&Series<f64>> for &Series<f64> {
            type Output = Series<f64>;
            fn $trait_method(self, rhs: &Series<f64>) -> Series<f64> {
                self.$method(rhs)
            }
        }

        impl $trait_name<Series<f64>> for Series<f64> {
            type Output = Series<f64>;
            fn $trait_method(self, rhs: Series<f64>) -> Series<f64> {
                self.$method(&rhs)
            }
        }
    };
}

impl_series_ops!(Add, add, add_series);
impl_series_ops!(Mul, mul, mul_series);
impl_series_ops!(Div, div, div_series);
impl_series_ops!(Sub, sub, sub_series);

macro_rules! impl_scalar_ops {
    ($trait_name:ident, $trait_method:ident, $method:ident) => {
        impl $trait_name<&Series<f64>> for f64 {
            type Output = Series<f64>;
            fn $trait_method(self, rhs: &Series<f64>) -> Series<f64> {
                rhs.$method(self)
            }
        }

        impl $trait_name<Series<f64>> for f64 {
            type Output = Series<f64>;
            fn $trait_method(self, rhs: Series<f64>) -> Series<f64> {
                rhs.$method(self)
            }
        }

        impl $trait_name<f64> for &Series<f64> {
            type Output = Series<f64>;
            fn $trait_method(self, scalar: f64) -> Series<f64> {
                self.$method(scalar)
            }
        }

        impl $trait_name<f64> for Series<f64> {
            type Output = Series<f64>;
            fn $trait_method(self, scalar: f64) -> Series<f64> {
                self.$method(scalar)
            }
        }
    };
}

impl Div<f64> for &Series<f64> {
    type Output = Series<f64>;

    fn div(self, scalar: f64) -> Series<f64> {
        self.div_scalar(scalar)
    }
}

impl Div<f64> for Series<f64> {
    type Output = Series<f64>;

    fn div(self, scalar: f64) -> Series<f64> {
        self.div_scalar(scalar)
    }
}

impl Div<&Series<f64>> for f64 {
    type Output = Series<f64>;

    fn div(self, rhs: &Series<f64>) -> Series<f64> {
        let scalars = vec![self; rhs.len()];
        Series::from(&scalars).div_series(&rhs)
    }
}

impl Div<Series<f64>> for f64 {
    type Output = Series<f64>;

    fn div(self, rhs: Series<f64>) -> Series<f64> {
        let scalars = vec![self; rhs.len()];
        Series::from(&scalars).div_series(&rhs)
    }
}

impl Sub<f64> for &Series<f64> {
    type Output = Series<f64>;

    fn sub(self, scalar: f64) -> Series<f64> {
        self.sub_scalar(scalar)
    }
}

impl Sub<f64> for Series<f64> {
    type Output = Series<f64>;

    fn sub(self, scalar: f64) -> Series<f64> {
        self.sub_scalar(scalar)
    }
}

impl Sub<&Series<f64>> for f64 {
    type Output = Series<f64>;

    fn sub(self, rhs: &Series<f64>) -> Series<f64> {
        rhs.neg().sub_scalar(-self)
    }
}

impl Sub<Series<f64>> for f64 {
    type Output = Series<f64>;

    fn sub(self, rhs: Series<f64>) -> Series<f64> {
        rhs.neg().sub_scalar(-self)
    }
}

impl_scalar_ops!(Add, add, add_scalar);
impl_scalar_ops!(Mul, mul, mul_scalar);

impl Mul<&Series<f64>> for &Series<bool> {
    type Output = Series<f64>;

    fn mul(self, rhs: &Series<f64>) -> Series<f64> {
        self.mul_series(rhs)
    }
}

impl Mul<&Series<f64>> for Series<bool> {
    type Output = Series<f64>;

    fn mul(self, rhs: &Series<f64>) -> Series<f64> {
        self.mul_series(rhs)
    }
}
