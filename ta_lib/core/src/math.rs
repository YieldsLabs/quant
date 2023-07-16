use crate::series::Series;

impl Series<f64> {
    fn ew<F>(&self, period: usize, alpha_fn: F) -> Self
    where
        F: Fn(usize) -> f64,
    {
        let len = self.len();

        let alpha = alpha_fn(period);

        let one_minus_alpha = 1.0 - alpha;

        let mut ew = Series::empty(len);
        ew[0] = self[0];

        for i in 1..len {
            if let (Some(ew_prev), Some(current)) = (ew[i - 1], self[i]) {
                ew[i] = Some(alpha * current + one_minus_alpha * ew_prev);
            }
        }

        ew
    }

    pub fn max(&self, scalar: f64) -> Self {
        self.fmap(|val| val.map(|v| v.max(scalar)).or(Some(scalar)))
    }

    pub fn min(&self, scalar: f64) -> Self {
        self.fmap(|val| val.map(|v| v.min(scalar)).or(Some(scalar)))
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

    pub fn ma(&self, period: usize) -> Self {
        self.sliding_map(period, |window, size, _| {
            Some(window.iter().filter_map(|v| *v).sum::<f64>() / size as f64)
        })
    }

    pub fn ema(&self, period: usize) -> Self {
        self.ew(period, |period| 2.0 / (period as f64 + 1.0))
    }

    pub fn smma(&self, period: usize) -> Self {
        self.ew(period, |period| 1.0 / (period as f64))
    }

    pub fn variance(&self, period: usize) -> Self {
        let ma = self.ma(period);

        self.sliding_map(period, |window, size, i| {
            let ma_val = ma[i].unwrap_or(0.0);
            let variance = window
                .iter()
                .filter_map(|v| *v)
                .map(|v| (v - ma_val).powi(2))
                .sum::<f64>()
                / size as f64;
            Some(variance)
        })
    }

    pub fn std(&self, period: usize) -> Self {
        self.variance(period).fmap(|val| val.map(|v| v.sqrt()))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_max() {
        let source = vec![
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ];
        let length = 1;
        let epsilon = 0.001;
        let expected = vec![
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

        let result = series.change(length).max(0.0);

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
        let source = vec![
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ];
        let length = 1;
        let epsilon = 0.001;
        let expected = vec![
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

        let result = series.change(length).min(0.0);

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
    fn test_ma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![Some(1.0), Some(1.5), Some(2.0), Some(3.0), Some(4.0)];
        let series = Series::from(&source);

        let result = series.ma(3);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_std() {
        let source = vec![2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0];
        let series = Series::from(&source);
        let period = 3;
        let epsilon = 0.001;
        let expected = vec![
            Some(0.0),
            Some(1.0),
            Some(1.6329),
            Some(1.6329),
            Some(1.6329),
            Some(0.8164),
            Some(0.8164),
            Some(0.8164),
            Some(0.8164),
            Some(0.8164),
            Some(0.8164),
        ];

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
}
