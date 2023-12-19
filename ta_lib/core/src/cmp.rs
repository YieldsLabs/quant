use crate::series::Series;
use crate::traits::Comparator;

impl Comparator<f32> for Series<f32> {
    type Output = Series<bool>;

    fn compare<F>(&self, scalar: &f32, comparator: F) -> Self::Output
    where
        F: Fn(f32, f32) -> bool,
    {
        self.fmap(|x| match x {
            Some(val) => Some(comparator(*val, *scalar)),
            None => Some(comparator(f32::NAN, *scalar)),
        })
    }

    fn seq(&self, rhs: &f32) -> Self::Output {
        self.compare(rhs, |a, b| a == b)
    }

    fn sne(&self, rhs: &f32) -> Self::Output {
        self.compare(rhs, |a, b| a != b)
    }

    fn sgt(&self, rhs: &f32) -> Self::Output {
        self.compare(rhs, |a, b| a > b)
    }

    fn sge(&self, rhs: &f32) -> Self::Output {
        self.compare(rhs, |a, b| a >= b)
    }

    fn slt(&self, rhs: &f32) -> Self::Output {
        self.compare(rhs, |a, b| a < b)
    }

    fn sle(&self, rhs: &f32) -> Self::Output {
        self.compare(rhs, |a, b| a <= b)
    }
}

impl Comparator<Series<f32>> for Series<f32> {
    type Output = Series<bool>;

    fn compare<F>(&self, rhs: &Series<f32>, comparator: F) -> Self::Output
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

    fn seq(&self, rhs: &Series<f32>) -> Self::Output {
        self.compare(rhs, |a, b| a == b)
    }

    fn sne(&self, rhs: &Series<f32>) -> Self::Output {
        self.compare(rhs, |a, b| a != b)
    }

    fn sgt(&self, rhs: &Series<f32>) -> Self::Output {
        self.compare(rhs, |a, b| a > b)
    }

    fn sge(&self, rhs: &Series<f32>) -> Self::Output {
        self.compare(rhs, |a, b| a >= b)
    }

    fn slt(&self, rhs: &Series<f32>) -> Self::Output {
        self.compare(rhs, |a, b| a < b)
    }

    fn sle(&self, rhs: &Series<f32>) -> Self::Output {
        self.compare(rhs, |a, b| a <= b)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_scalar_eq() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = 1.0;
        let expected: Series<bool> = Series::from([0.0, 0.0, 0.0, 1.0, 0.0]).into();

        let result = a.seq(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_scalar_ne() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = 1.0;
        let expected: Series<bool> = Series::from([1.0, 1.0, 1.0, 0.0, 1.0]).into();

        let result = a.sne(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_scalar_gt() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 4.0, 5.0]);
        let b = 1.0;
        let expected: Series<bool> = Series::from([0.0, 1.0, 1.0, 1.0, 1.0]).into();

        let result = a.sgt(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_scalar_ge() {
        let a = Series::from([f32::NAN, 2.0, 1.0, 1.0, 5.0]);
        let b = 1.0;
        let expected: Series<bool> = Series::from([0.0, 1.0, 1.0, 1.0, 1.0]).into();

        let result = a.sge(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_scalar_lt() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 4.0, 5.0]);
        let b = 1.0;
        let expected: Series<bool> = Series::from([0.0, 0.0, 0.0, 0.0, 0.0]).into();

        let result = a.slt(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_scalar_le() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = 1.0;
        let expected: Series<bool> = Series::from([0.0, 0.0, 0.0, 1.0, 0.0]).into();

        let result = a.sle(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_series_eq() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 0.0, 0.0, 1.0, 0.0]).into();

        let result = a.seq(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_series_ne() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([1.0, 1.0, 1.0, 0.0, 1.0]).into();

        let result = a.sne(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_series_gt() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 4.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 1.0, 0.0, 1.0, 1.0]).into();

        let result = a.sgt(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_series_ge() {
        let a = Series::from([f32::NAN, 2.0, 1.0, 1.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 1.0, 0.0, 1.0, 1.0]).into();

        let result = a.sge(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_series_lt() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 4.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 0.0, 1.0, 0.0, 0.0]).into();

        let result = a.slt(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_series_le() {
        let a = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Series<bool> = Series::from([0.0, 0.0, 1.0, 1.0, 0.0]).into();

        let result = a.sle(&b);

        assert_eq!(result, expected);
    }

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
