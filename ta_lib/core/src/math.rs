use crate::series::Series;

impl Series<f64> {
    pub fn window<F>(&self, period: usize, f: F) -> Self
    where
        F: Fn(&[f64], usize, usize) -> f64,
    {
        let len = self.len();
        let mut result = Self::empty(len);
        let mut window = vec![0.0; period];
        let mut pos = 0;

        for i in 0..len {
            if let Some(value) = self[i] {
                window[pos] = value;

                let size = (i + 1).min(period);

                result[i] = Some(f(&window[0..size], size, i));

                pos = (pos + 1) % period;
            }
        }

        result
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
        self.window(period, |window, _, _| window.iter().sum())
    }

    pub fn mean(&self, period: usize) -> Self {
        self.window(period, |window, size, _| {
            window.iter().sum::<f64>() / size as f64
        })
    }

    pub fn std(&self, period: usize) -> Self {
        let mean = self.mean(period);

        self.window(period, |window, size, i| {
            let mean_val = mean[i].unwrap_or(0.0);
            let variance =
                window.iter().map(|&v| (v - mean_val).powi(2)).sum::<f64>() / size as f64;
            variance.sqrt()
        })
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
    fn test_mean() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![Some(1.0), Some(1.5), Some(2.0), Some(3.0), Some(4.0)];
        let series = Series::from(&source);

        let result = series.mean(3);

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
