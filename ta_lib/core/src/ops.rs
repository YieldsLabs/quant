use crate::series::Series;
use std::ops::{Add, Div, Mul, Neg, Sub};

impl Series<f64> {
    pub fn add_series(&self, rhs: &Series<f64>) -> Series<f64> {
        self.clone().zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(a_val + b_val),
            _ => None,
        })
    }

    pub fn mul_series(&self, rhs: &Series<f64>) -> Series<f64> {
        self.clone().zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(a_val * b_val),
            _ => None,
        })
    }

    pub fn div_series(&self, rhs: &Series<f64>) -> Series<f64> {
        self.clone().zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => {
                if b_val == 0.0 {
                    if a_val > 0.0 {
                        Some(std::f64::INFINITY)
                    } else if a_val < 0.0 {
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
        self.clone().zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(a_val - b_val),
            _ => None,
        })
    }

    pub fn add_scalar(&self, scalar: f64) -> Series<f64> {
        self.fmap(|val| val.map(|v| v + scalar))
    }

    pub fn mul_scalar(&self, scalar: f64) -> Series<f64> {
        self.fmap(|val| val.map(|v| v * scalar))
    }

    pub fn div_scalar(&self, scalar: f64) -> Series<f64> {
        self.fmap(|val| {
            val.map(|v| {
                if *v == 0.0 {
                    if scalar > 0.0 {
                        std::f64::INFINITY
                    } else if scalar < 0.0 {
                        std::f64::NEG_INFINITY
                    } else {
                        0.0
                    }
                } else {
                    v / scalar
                }
            })
        })
    }

    pub fn sub_scalar(&self, scalar: f64) -> Series<f64> {
        self.fmap(|val| val.map(|v| v - scalar))
    }

    pub fn neg(&self) -> Series<f64> {
        self.fmap(|val| val.map(|v| if *v == 0.0 { *v } else { -*v }))
    }
}

impl Series<bool> {
    pub fn mul_series(&self, rhs: &Series<f64>) -> Series<f64> {
        self.clone().zip_with(rhs, |b, val| match (b, val) {
            (Some(b_val), Some(val_val)) => {
                if b_val {
                    Some(val_val)
                } else {
                    Some(0.0)
                }
            }
            _ => None,
        })
    }
}

impl Add<Series<f64>> for &Series<f64> {
    type Output = Series<f64>;

    fn add(self, rhs: Series<f64>) -> Series<f64> {
        self.add_series(&rhs)
    }
}

impl Add<&Series<f64>> for Series<f64> {
    type Output = Series<f64>;

    fn add(self, rhs: &Series<f64>) -> Series<f64> {
        self.add_series(rhs)
    }
}

impl Add<&Series<f64>> for &Series<f64> {
    type Output = Series<f64>;

    fn add(self, rhs: &Series<f64>) -> Series<f64> {
        self.add_series(rhs)
    }
}

impl Mul<Series<f64>> for &Series<f64> {
    type Output = Series<f64>;

    fn mul(self, rhs: Series<f64>) -> Series<f64> {
        self.mul_series(&rhs)
    }
}

impl Mul<&Series<f64>> for Series<f64> {
    type Output = Series<f64>;

    fn mul(self, rhs: &Series<f64>) -> Series<f64> {
        self.mul_series(rhs)
    }
}

impl Mul<&Series<f64>> for &Series<f64> {
    type Output = Series<f64>;

    fn mul(self, rhs: &Series<f64>) -> Series<f64> {
        self.mul_series(rhs)
    }
}

impl Div<&Series<f64>> for &Series<f64> {
    type Output = Series<f64>;

    fn div(self, rhs: &Series<f64>) -> Series<f64> {
        self.div_series(rhs)
    }
}

impl Div<&Series<f64>> for Series<f64> {
    type Output = Series<f64>;

    fn div(self, rhs: &Series<f64>) -> Series<f64> {
        self.div_series(rhs)
    }
}

impl Div<Series<f64>> for &Series<f64> {
    type Output = Series<f64>;

    fn div(self, rhs: Series<f64>) -> Series<f64> {
        self.div_series(&rhs)
    }
}

impl Sub<&Series<f64>> for Series<f64> {
    type Output = Series<f64>;

    fn sub(self, rhs: &Series<f64>) -> Series<f64> {
        self.sub_series(rhs)
    }
}

impl Sub<Series<f64>> for &Series<f64> {
    type Output = Series<f64>;

    fn sub(self, rhs: Series<f64>) -> Series<f64> {
        self.sub_series(&rhs)
    }
}

impl Sub<&Series<f64>> for &Series<f64> {
    type Output = Series<f64>;

    fn sub(self, rhs: &Series<f64>) -> Series<f64> {
        self.sub_series(rhs)
    }
}

impl Add<f64> for &Series<f64> {
    type Output = Series<f64>;

    fn add(self, scalar: f64) -> Series<f64> {
        self.add_scalar(scalar)
    }
}

impl Mul<f64> for &Series<f64> {
    type Output = Series<f64>;

    fn mul(self, scalar: f64) -> Series<f64> {
        self.mul_scalar(scalar)
    }
}

impl Mul<f64> for Series<f64> {
    type Output = Series<f64>;

    fn mul(self, scalar: f64) -> Series<f64> {
        self.mul_scalar(scalar)
    }
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

impl Sub<f64> for &Series<f64> {
    type Output = Series<f64>;

    fn sub(self, scalar: f64) -> Series<f64> {
        self.sub_scalar(scalar)
    }
}

impl Add<&Series<f64>> for f64 {
    type Output = Series<f64>;

    fn add(self, rhs: &Series<f64>) -> Series<f64> {
        rhs.add_scalar(self)
    }
}

impl Add<Series<f64>> for f64 {
    type Output = Series<f64>;

    fn add(self, rhs: Series<f64>) -> Series<f64> {
        rhs.add_scalar(self)
    }
}

impl Mul<&Series<f64>> for f64 {
    type Output = Series<f64>;

    fn mul(self, rhs: &Series<f64>) -> Series<f64> {
        rhs.mul_scalar(self)
    }
}

impl Mul<Series<f64>> for f64 {
    type Output = Series<f64>;

    fn mul(self, rhs: Series<f64>) -> Series<f64> {
        rhs.mul_scalar(self)
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

impl Neg for &Series<f64> {
    type Output = Series<f64>;

    fn neg(self) -> Series<f64> {
        self.neg()
    }
}
