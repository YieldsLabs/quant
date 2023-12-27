use crate::series::Series;
use crate::traits::Extremum;

impl Extremum<f32> for Series<f32> {
    type Output = Series<f32>;

    fn extremum<F>(&self, scalar: &f32, f: F) -> Self::Output
    where
        F: Fn(f32, f32) -> f32,
    {
        self.fmap(|val| val.map(|v| f(*v, *scalar)).or_else(|| Some(*scalar)))
    }

    fn max(&self, scalar: &f32) -> Self::Output {
        self.extremum(scalar, f32::max)
    }

    fn min(&self, scalar: &f32) -> Self::Output {
        self.extremum(scalar, f32::min)
    }
}

impl Extremum<Series<f32>> for Series<f32> {
    type Output = Series<f32>;

    fn extremum<F>(&self, rhs: &Series<f32>, f: F) -> Self::Output
    where
        F: Fn(f32, f32) -> f32,
    {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(f(*a_val, *b_val)),
            (Some(a_val), None) | (None, Some(a_val)) => Some(*a_val),
            _ => None,
        })
    }

    fn max(&self, rhs: &Series<f32>) -> Self::Output {
        self.extremum(rhs, f32::max)
    }

    fn min(&self, rhs: &Series<f32>) -> Self::Output {
        self.extremum(rhs, f32::min)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_smax() {
        let source = vec![
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ];
        let length = 1;
        let epsilon = 0.001;
        let expected = [
            Some(0.0),
            Some(0.0),
            Some(0.0599),
            Some(0.0),
            Some(0.7199),
            Some(0.5),
            Some(0.2700),
            Some(0.3200),
            Some(0.4200),
        ];
        let series = Series::from(&source);

        let result = series.change(length).max(&0.0);

        for i in 0..result.len() {
            match (result[i], expected[i]) {
                (Some(a), Some(b)) => {
                    assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b)
                }
                (None, None) => {}
                _ => panic!("at position {}: {:?} != {:?}", i, result[i], expected[i]),
            }
        }
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
        let source = vec![
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ];
        let length = 1;
        let epsilon = 0.001;
        let expected = [
            Some(0.0),
            Some(-0.25),
            Some(0.0),
            Some(-0.5399),
            Some(0.0),
            Some(0.0),
            Some(0.0),
            Some(0.0),
            Some(0.0),
        ];
        let series = Series::from(&source);

        let result = series.change(length).min(&0.0);

        for i in 0..result.len() {
            match (result[i], expected[i]) {
                (Some(a), Some(b)) => {
                    assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b)
                }
                (None, None) => {}
                _ => panic!("at position {}: {:?} != {:?}", i, result[i], expected[i]),
            }
        }
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
}
