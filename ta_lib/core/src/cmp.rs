use crate::constants::NAN;
use crate::traits::Comparator;
use crate::types::{Price, Rule, Scalar};

impl Comparator<Scalar> for Price {
    type Output = Rule;

    fn compare<F>(&self, scalar: &Scalar, comparator: F) -> Self::Output
    where
        F: Fn(Scalar, Scalar) -> bool,
    {
        self.fmap(|x| {
            x.map_or(Some(comparator(NAN, *scalar)), |val| {
                Some(comparator(*val, *scalar))
            })
        })
    }

    fn seq(&self, rhs: &Scalar) -> Self::Output {
        self.compare(rhs, |a, b| a == b)
    }

    fn sne(&self, rhs: &Scalar) -> Self::Output {
        self.compare(rhs, |a, b| a != b)
    }

    fn sgt(&self, rhs: &Scalar) -> Self::Output {
        self.compare(rhs, |a, b| a > b)
    }

    fn sgte(&self, rhs: &Scalar) -> Self::Output {
        self.compare(rhs, |a, b| a >= b)
    }

    fn slt(&self, rhs: &Scalar) -> Self::Output {
        self.compare(rhs, |a, b| a < b)
    }

    fn slte(&self, rhs: &Scalar) -> Self::Output {
        self.compare(rhs, |a, b| a <= b)
    }
}

impl Comparator<Price> for Price {
    type Output = Rule;

    fn compare<F>(&self, rhs: &Price, comparator: F) -> Self::Output
    where
        F: Fn(Scalar, Scalar) -> bool,
    {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(comparator(*a_val, *b_val)),
            (None, Some(b_val)) => Some(comparator(NAN, *b_val)),
            (Some(a_val), None) => Some(comparator(*a_val, NAN)),
            _ => None,
        })
    }

    fn seq(&self, rhs: &Price) -> Self::Output {
        self.compare(rhs, |a, b| a == b)
    }

    fn sne(&self, rhs: &Price) -> Self::Output {
        self.compare(rhs, |a, b| a != b)
    }

    fn sgt(&self, rhs: &Price) -> Self::Output {
        self.compare(rhs, |a, b| a > b)
    }

    fn sgte(&self, rhs: &Price) -> Self::Output {
        self.compare(rhs, |a, b| a >= b)
    }

    fn slt(&self, rhs: &Price) -> Self::Output {
        self.compare(rhs, |a, b| a < b)
    }

    fn slte(&self, rhs: &Price) -> Self::Output {
        self.compare(rhs, |a, b| a <= b)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::series::Series;

    #[test]
    fn test_scalar_eq() {
        let a = Series::from([NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = 1.0;
        let expected: Rule = Series::from([0.0, 0.0, 0.0, 1.0, 0.0]).into();

        let result = a.seq(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_scalar_ne() {
        let a = Series::from([NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = 1.0;
        let expected: Rule = Series::from([1.0, 1.0, 1.0, 0.0, 1.0]).into();

        let result = a.sne(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_scalar_gt() {
        let a = Series::from([NAN, 2.0, 3.0, 4.0, 5.0]);
        let b = 1.0;
        let expected: Rule = Series::from([0.0, 1.0, 1.0, 1.0, 1.0]).into();

        let result = a.sgt(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_scalar_gte() {
        let a = Series::from([NAN, 2.0, 1.0, 1.0, 5.0]);
        let b = 1.0;
        let expected: Rule = Series::from([0.0, 1.0, 1.0, 1.0, 1.0]).into();

        let result = a.sgte(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_scalar_lt() {
        let a = Series::from([NAN, 2.0, 3.0, 4.0, 5.0]);
        let b = 1.0;
        let expected: Rule = Series::from([0.0, 0.0, 0.0, 0.0, 0.0]).into();

        let result = a.slt(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_scalar_lte() {
        let a = Series::from([NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = 1.0;
        let expected: Rule = Series::from([0.0, 0.0, 0.0, 1.0, 0.0]).into();

        let result = a.slte(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_series_eq() {
        let a = Series::from([NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Rule = Series::from([0.0, 0.0, 0.0, 1.0, 0.0]).into();

        let result = a.seq(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_series_ne() {
        let a = Series::from([NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Rule = Series::from([1.0, 1.0, 1.0, 0.0, 1.0]).into();

        let result = a.sne(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_series_gt() {
        let a = Series::from([NAN, 2.0, 3.0, 4.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Rule = Series::from([0.0, 1.0, 0.0, 1.0, 1.0]).into();

        let result = a.sgt(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_series_gte() {
        let a = Series::from([NAN, 2.0, 1.0, 1.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Rule = Series::from([0.0, 1.0, 0.0, 1.0, 1.0]).into();

        let result = a.sgte(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_series_lt() {
        let a = Series::from([NAN, 2.0, 3.0, 4.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Rule = Series::from([0.0, 0.0, 1.0, 0.0, 0.0]).into();

        let result = a.slt(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_series_lte() {
        let a = Series::from([NAN, 2.0, 3.0, 1.0, 5.0]);
        let b = Series::from([1.0, 1.0, 6.0, 1.0, 1.0]);
        let expected: Rule = Series::from([0.0, 0.0, 1.0, 1.0, 0.0]).into();

        let result = a.slte(&b);

        assert_eq!(result, expected);
    }
}
