use crate::series::Series;
use crate::traits::Bitwise;
use std::ops::{BitAnd, BitOr};

impl Bitwise<Series<bool>> for Series<bool> {
    type Output = Series<bool>;

    fn op<F>(&self, rhs: &Series<bool>, operation: F) -> Self::Output
    where
        F: Fn(&bool, &bool) -> bool,
    {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(operation(a_val, b_val)),
            (Some(_), None) | (None, Some(_)) | (None, None) => Some(false),
        })
    }

    fn sand(&self, rhs: &Series<bool>) -> Self::Output {
        self.op(rhs, |a, b| a & b)
    }

    fn sor(&self, rhs: &Series<bool>) -> Self::Output {
        self.op(rhs, |a, b| a | b)
    }
}

impl BitAnd for Series<bool> {
    type Output = Self;

    fn bitand(self, rhs: Self) -> Self::Output {
        self.sand(&rhs)
    }
}

impl BitOr for Series<bool> {
    type Output = Self;

    fn bitor(self, rhs: Self) -> Self::Output {
        self.sor(&rhs)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::traits::Comparator;

    #[test]
    fn test_bitand() {
        let a = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 0.0, 0.0, 0.0, 0.0]).into();

        let result = a.sgt(&b) & a.slt(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_bitor() {
        let a = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let b = Series::from([1.0, 1.0, 1.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 1.0, 1.0, 1.0, 1.0]).into();

        let result = a.sgt(&b) | a.slt(&b);

        assert_eq!(result, expected);
    }
}
