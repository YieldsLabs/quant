use crate::traits::Extremum;
use crate::types::{Price, Scalar};

impl Extremum<Scalar> for Price {
    type Output = Price;

    fn extremum<F>(&self, scalar: &Scalar, f: F) -> Self::Output
    where
        F: Fn(Scalar, Scalar) -> Scalar,
    {
        self.fmap(|val| val.map(|v| f(*v, *scalar)).or(Some(*scalar)))
    }

    fn max(&self, scalar: &Scalar) -> Self::Output {
        self.extremum(scalar, Scalar::max)
    }

    fn min(&self, scalar: &Scalar) -> Self::Output {
        self.extremum(scalar, Scalar::min)
    }

    fn clip(&self, lhs: &Scalar, rhs: &Scalar) -> Self::Output {
        self.min(rhs).max(lhs)
    }
}

impl Extremum<Price> for Price {
    type Output = Price;

    fn extremum<F>(&self, rhs: &Price, f: F) -> Self::Output
    where
        F: Fn(Scalar, Scalar) -> Scalar,
    {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(f(*a_val, *b_val)),
            (Some(a_val), None) | (None, Some(a_val)) => Some(*a_val),
            _ => None,
        })
    }

    fn max(&self, rhs: &Price) -> Self::Output {
        self.extremum(rhs, Scalar::max)
    }

    fn min(&self, rhs: &Price) -> Self::Output {
        self.extremum(rhs, Scalar::min)
    }

    fn clip(&self, lhs: &Price, rhs: &Price) -> Self::Output {
        self.min(rhs).max(lhs)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::series::Series;

    #[test]
    fn test_smax() {
        let series = Series::from([
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ]);
        let length = 1;
        let expected = Series::from([
            0.,
            0.,
            0.060001373,
            0.,
            0.7200012,
            0.5,
            0.26999664,
            0.3199997,
            0.42000198,
        ]);

        let result = series.change(length).max(&0.0);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_max() {
        let a = Series::from([
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ]);
        let b = Series::from([34.34, 44.0, 45.15, 43.60, 14.33, 56.83, 45.10, 45.42, 46.84]);
        let expected = Series::from([
            44.34, 44.09, 45.15, 43.61, 44.33, 56.83, 45.10, 45.42, 46.84,
        ]);

        let result = a.max(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_max_nan() {
        let a = Series::from([
            f32::NAN,
            44.09,
            44.15,
            43.61,
            44.33,
            44.83,
            45.10,
            45.42,
            45.84,
        ]);
        let b = Series::from([34.34, 44.0, 45.15, 43.60, 14.33, 56.83, 45.10, 45.42, 46.84]);
        let expected = Series::from([
            34.34, 44.09, 45.15, 43.61, 44.33, 56.83, 45.10, 45.42, 46.84,
        ]);

        let result = a.max(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_smin() {
        let series = Series::from([
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ]);
        let length = 1;
        let expected = Series::from([0., -0.25, 0., -0.5400009, 0., 0., 0., 0., 0.]);

        let result = series.change(length).min(&0.0);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_min() {
        let a = Series::from([
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ]);
        let b = Series::from([34.34, 44.0, 45.15, 43.60, 14.33, 56.83, 45.10, 45.42, 46.84]);
        let expected = Series::from([34.34, 44.0, 44.15, 43.60, 14.33, 44.83, 45.10, 45.42, 45.84]);

        let result = a.min(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_min_nan() {
        let a = Series::from([
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ]);
        let b = Series::from([
            f32::NAN,
            44.0,
            45.15,
            43.60,
            14.33,
            56.83,
            45.10,
            45.42,
            46.84,
        ]);
        let expected = Series::from([44.34, 44.0, 44.15, 43.60, 14.33, 44.83, 45.10, 45.42, 45.84]);

        let result = a.min(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_clip() {
        let source = Series::from([-1.0, 0.0, 1.0, 3.0, 5.0]);
        let expected = Series::from([0.0, 0.0, 1.0, 3.0, 3.0]);
        let min = 0.;
        let max = 3.;

        let result = source.clip(&min, &max);

        assert_eq!(result, expected);
    }
}
