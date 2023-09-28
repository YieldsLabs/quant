use crate::series::Series;
use std::ops::{BitAnd, BitOr};

macro_rules! scalar_comparison {
    ($($name:ident, $op:tt);* $(;)?) => {
        $(
            pub fn $name(&self, scalar: f32) -> Series<bool> {
                self.compare_scalar(scalar, |a, b| a $op b)
            }
        )*
    };
}

macro_rules! series_comparison {
    ($($name:ident, $op:tt);* $(;)?) => {
        $(
            pub fn $name(&self, rhs: &Series<f32>) -> Series<bool> {
                self.compare(rhs, |a, b| a $op b)
            }
        )*
    };
}

macro_rules! logical_operation {
    ($($name:ident, $op:tt);* $(;)?) => {
        $(
            pub fn $name(&self, rhs: &Series<bool>) -> Series<bool> {
                self.logical_op(rhs, |a, b| a $op b)
            }
        )*
    };
}

impl Series<f32> {
    fn compare_scalar<F>(&self, scalar: f32, comparator: F) -> Series<bool>
    where
        F: Fn(f32, f32) -> bool,
    {
        self.fmap(|x| match x {
            Some(val) => Some(comparator(*val, scalar)),
            None => Some(comparator(f32::NAN, scalar)),
        })
    }

    fn compare<F>(&self, rhs: &Series<f32>, comparator: F) -> Series<bool>
    where
        F: Fn(f32, f32) -> bool,
    {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(comparator(*a_val, *b_val)),
            (None, Some(b_val)) => Some(comparator(f32::NAN, *b_val)),
            (Some(a_val), None) => Some(comparator(*a_val, f32::NAN)),
            _ => None,
        })
    }

    scalar_comparison! {
        seq, ==;
        sne, !=;
        sgt, >;
        sgte, >=;
        slt, <;
        slte, <=;
    }

    series_comparison! {
        eq, ==;
        ne, !=;
        gt, >;
        gte, >=;
        lt, <;
        lte, <=;
    }
}

impl Series<bool> {
    fn logical_op<F>(&self, rhs: &Series<bool>, operation: F) -> Series<bool>
    where
        F: Fn(bool, bool) -> bool,
    {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(operation(*a_val, *b_val)),
            _ => None,
        })
    }

    logical_operation! {
        and, &;
        or, |;
    }
}

impl BitAnd for Series<bool> {
    type Output = Self;

    fn bitand(self, rhs: Self) -> Self::Output {
        self.and(&rhs)
    }
}

impl BitOr for Series<bool> {
    type Output = Self;

    fn bitor(self, rhs: Self) -> Self::Output {
        self.or(&rhs)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_seq() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = 1.0;
        let expected: Series<bool> = Series::from([0.0, 0.0, 0.0, 1.0, 0.0]).into();

        let result = a.seq(b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_sne() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = 1.0;
        let expected: Series<bool> = Series::from([1.0, 1.0, 1.0, 0.0, 1.0]).into();

        let result = a.sne(b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_sgt() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 4.0, 5.0]);
        let b = 1.0;
        let expected: Series<bool> = Series::from([0.0, 1.0, 1.0, 1.0, 1.0]).into();

        let result = a.sgt(b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_sgte() {
        let a = Series::from([f32::NAN, 2.0, 1.0, 1.0, 5.0]);
        let b = 1.0;
        let expected: Series<bool> = Series::from([0.0, 1.0, 1.0, 1.0, 1.0]).into();

        let result = a.sgte(b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_slt() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 4.0, 5.0]);
        let b = 1.0;
        let expected: Series<bool> = Series::from([0.0, 0.0, 0.0, 0.0, 0.0]).into();

        let result = a.slt(b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_slte() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = 1.0;
        let expected: Series<bool> = Series::from([0.0, 0.0, 0.0, 1.0, 0.0]).into();

        let result = a.slte(b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_eq() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 0.0, 0.0, 1.0, 0.0]).into();

        let result = a.eq(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_ne() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([1.0, 1.0, 1.0, 0.0, 1.0]).into();

        let result = a.ne(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_gt() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 4.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 1.0, 0.0, 1.0, 1.0]).into();

        let result = a.gt(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_gte() {
        let a = Series::from([f32::NAN, 2.0, 1.0, 1.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 1.0, 0.0, 1.0, 1.0]).into();

        let result = a.gte(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_lt() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 4.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 0.0, 1.0, 0.0, 0.0]).into();

        let result = a.lt(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_lte() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 0.0, 1.0, 1.0, 0.0]).into();

        let result = a.lte(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_bitand() {
        let a = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 0.0, 0.0, 0.0, 0.0]).into();

        let result = a.gt(&b) & a.lt(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_bitor() {
        let a = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let b = Series::from([1.0, 1.0, 1.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 1.0, 1.0, 1.0, 1.0]).into();

        let result = a.gt(&b) | a.lt(&b);

        assert_eq!(result, expected);
    }
}
