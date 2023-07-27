use crate::series::Series;
use std::ops::{BitAnd, BitOr};

impl Series<f64> {
    fn compare_series<F>(&self, rhs: &Series<f64>, f: F) -> Series<bool>
    where
        F: Fn(f64, f64) -> bool,
    {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(f(*a_val, *b_val)),
            _ => None,
        })
    }

    fn compare<F>(&self, scalar: f64, f: F) -> Series<bool>
    where
        F: Fn(f64, f64) -> bool,
    {
        self.fmap(|x| x.map(|v| f(*v, scalar)))
    }

    pub fn eq(&self, scalar: f64) -> Series<bool> {
        self.compare(scalar, |a, b| a == b)
    }

    pub fn ne(&self, scalar: f64) -> Series<bool> {
        self.compare(scalar, |a, b| a != b)
    }

    pub fn gt(&self, scalar: f64) -> Series<bool> {
        self.compare(scalar, |a, b| a > b)
    }

    pub fn gte(&self, scalar: f64) -> Series<bool> {
        self.compare(scalar, |a, b| a >= b)
    }

    pub fn lt(&self, scalar: f64) -> Series<bool> {
        self.compare(scalar, |a, b| a < b)
    }

    pub fn lte(&self, scalar: f64) -> Series<bool> {
        self.compare(scalar, |a, b| a <= b)
    }

    pub fn eq_series(&self, rhs: &Series<f64>) -> Series<bool> {
        self.compare_series(rhs, |a, b| a == b)
    }

    pub fn ne_series(&self, rhs: &Series<f64>) -> Series<bool> {
        self.compare_series(rhs, |a, b| a != b)
    }

    pub fn gt_series(&self, rhs: &Series<f64>) -> Series<bool> {
        self.compare_series(rhs, |a, b| a > b)
    }

    pub fn gte_series(&self, rhs: &Series<f64>) -> Series<bool> {
        self.compare_series(rhs, |a, b| a >= b)
    }

    pub fn lt_series(&self, rhs: &Series<f64>) -> Series<bool> {
        self.compare_series(rhs, |a, b| a < b)
    }

    pub fn lte_series(&self, rhs: &Series<f64>) -> Series<bool> {
        self.compare_series(rhs, |a, b| a <= b)
    }
}

impl Series<bool> {
    pub fn and_series(&self, rhs: &Series<bool>) -> Series<bool> {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(*a_val & *b_val),
            _ => None,
        })
    }

    pub fn or_series(&self, rhs: &Series<bool>) -> Series<bool> {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(*a_val | *b_val),
            _ => None,
        })
    }
}

impl BitAnd for Series<bool> {
    type Output = Self;

    fn bitand(self, rhs: Self) -> Self::Output {
        self.and_series(&rhs)
    }
}

impl BitOr for Series<bool> {
    type Output = Self;

    fn bitor(self, rhs: Self) -> Self::Output {
        self.or_series(&rhs)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bitand() {
        let a = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 0.0, 0.0, 0.0, 0.0]).into();

        let result = a.gt_series(&b) & a.lt_series(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_bitor() {
        let a = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let b = Series::from([1.0, 1.0, 1.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 1.0, 1.0, 1.0, 1.0]).into();

        let result = a.gt_series(&b) | a.lt_series(&b);

        assert_eq!(result, expected);
    }
}
