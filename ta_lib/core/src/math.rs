use crate::series::Series;

impl Series<f32> {
    pub fn smax(&self, scalar: f32) -> Self {
        self.fmap(|val| val.map(|v| v.max(scalar)).or(Some(scalar)))
    }

    pub fn smin(&self, scalar: f32) -> Self {
        self.fmap(|val| val.map(|v| v.min(scalar)).or(Some(scalar)))
    }

    pub fn max(&self, rhs: &Series<f32>) -> Self {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(a_val.max(*b_val)),
            _ => None,
        })
    }

    pub fn min(&self, rhs: &Series<f32>) -> Self {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(a_val.min(*b_val)),
            _ => None,
        })
    }

    pub fn abs(&self) -> Self {
        self.fmap(|val| val.map(|v| v.abs()))
    }

    pub fn log(&self) -> Self {
        self.fmap(|val| match val {
            Some(v) if *v > 0.0 => Some(v.ln()),
            _ => None,
        })
    }

    pub fn exp(&self) -> Self {
        self.fmap(|val| val.map(|v| v.exp()))
    }

    pub fn sqrt(&self) -> Self {
        self.fmap(|val| val.filter(|&v| *v >= 0.0).map(|v| v.sqrt()))
    }

    pub fn round(&self, places: usize) -> Self {
        let multiplier = 10f32.powi(places as i32);
        self.fmap(|val| val.map(|v| (v * multiplier).round() / multiplier))
    }

    pub fn cumsum(&self) -> Self {
        let mut sum = 0.0;

        self.fmap(|val| {
            val.map(|v| {
                sum += v;
                sum
            })
        })
    }

    pub fn sum(&self, period: usize) -> Self {
        self.sliding_map(period, |window, _, _| {
            Some(window.iter().filter_map(|v| *v).sum())
        })
    }

    pub fn var(&self, period: usize) -> Self {
        let ma: Vec<f32> = self.ma(period).into();

        self.sliding_map(period, |window, size, i| {
            let ma_val = ma[i];
            let variance = window
                .iter()
                .filter_map(|v| *v)
                .map(|v| (v - ma_val).powi(2))
                .sum::<f32>()
                / size as f32;
            Some(variance)
        })
    }

    pub fn std(&self, period: usize) -> Self {
        self.var(period).sqrt()
    }

    pub fn md(&self, period: usize) -> Self {
        let ma: Vec<f32> = self.ma(period).into();
        self.sliding_map(period, |window, size, i| {
            let mean = ma[i];
            Some(
                window
                    .iter()
                    .filter_map(|v| *v)
                    .map(|v| (v - mean).abs())
                    .sum::<f32>()
                    / size as f32,
            )
        })
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
        let expected = [Some(0.0),
            Some(0.0),
            Some(0.0599),
            Some(0.0),
            Some(0.7199),
            Some(0.5),
            Some(0.2700),
            Some(0.3200),
            Some(0.4200)];
        let series = Series::from(&source);

        let result = series.change(length).smax(0.0);

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
    fn test_smin() {
        let source = vec![
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ];
        let length = 1;
        let epsilon = 0.001;
        let expected = [Some(0.0),
            Some(-0.25),
            Some(0.0),
            Some(-0.5399),
            Some(0.0),
            Some(0.0),
            Some(0.0),
            Some(0.0),
            Some(0.0)];
        let series = Series::from(&source);

        let result = series.change(length).smin(0.0);

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
    fn test_abs() {
        let source = vec![-1.0, 2.0, -3.0, 4.0, 5.0];
        let expected = vec![Some(1.0), Some(2.0), Some(3.0), Some(4.0), Some(5.0)];
        let series = Series::from(&source);

        let result = series.abs();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_sqrt() {
        let source = vec![-1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![
            None,
            Some(1.4142135),
            Some(1.7320508),
            Some(2.0),
            Some(2.236068),
        ];
        let series = Series::from(&source);

        let result = series.sqrt();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_log() {
        let source = vec![-1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![
            None,
            Some(0.6931472),
            Some(1.0986123),
            Some(1.3862944),
            Some(1.609438),
        ];
        let series = Series::from(&source);

        let result = series.log();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_exp() {
        let source = vec![-1.0, 2.0, -3.0, 4.0, 5.0];
        let expected = vec![
            Some(0.36787945),
            Some(7.389056),
            Some(0.049787067),
            Some(54.59815),
            Some(148.41316),
        ];
        let series = Series::from(&source);

        let result = series.exp();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_round() {
        let source = Series::from([-1.2211, 2.2456, -3.5677, 4.0, 5.3334]);
        let expected = Series::from([-1.0, 2.0, -4.0, 4.0, 5.0]);

        let result = source.round(0);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_cumsum() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![Some(1.0), Some(3.0), Some(6.0), Some(10.0), Some(15.0)];
        let series = Series::from(&source);

        let result = series.cumsum();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_sum() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![Some(1.0), Some(3.0), Some(6.0), Some(9.0), Some(12.0)];
        let series = Series::from(&source);

        let result = series.sum(3);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_std() {
        let source = vec![2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0];
        let series = Series::from(&source);
        let period = 3;
        let epsilon = 0.001;
        let expected = [Some(0.0),
            Some(1.0),
            Some(1.6329),
            Some(1.6329),
            Some(1.6329),
            Some(0.8164),
            Some(0.8164),
            Some(0.8164),
            Some(0.8164),
            Some(0.8164),
            Some(0.8164)];

        let result = series.std(period);

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
    fn test_md() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![
            Some(0.0),
            Some(0.5),
            Some(0.6666667),
            Some(0.6666667),
            Some(0.6666667),
        ];
        let series = Series::from(&source);

        let result = series.md(3);

        assert_eq!(result, expected);
    }
}
