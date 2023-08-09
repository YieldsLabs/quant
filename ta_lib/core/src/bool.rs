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
        self.fmap(|x| x.map(|v| comparator(*v, scalar)))
    }

    fn compare<F>(&self, rhs: &Series<f32>, comparator: F) -> Series<bool>
    where
        F: Fn(f32, f32) -> bool,
    {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(comparator(*a_val, *b_val)),
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
