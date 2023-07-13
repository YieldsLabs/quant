use crate::series::Series;

impl Series<f64> {
    pub fn max(&self, scalar: f64) -> Self {
        self.fmap(|val| match val {
            Some(v) => Some(v.max(scalar)),
            None => Some(scalar),
        })
    }

    pub fn min(&self, scalar: f64) -> Self {
        self.fmap(|val| match val {
            Some(v) => Some(v.min(scalar)),
            None => Some(scalar),
        })
    }

    pub fn cumsum(&self) -> Self {
        let len = self.len();
        let mut cumsum = Self::empty(len);

        let mut sum = 0.0;

        for i in 0..len {
            if let Some(val) = self[i] {
                sum += val;
                cumsum[i] = Some(sum);
            }
        }

        cumsum
    }

    pub fn sum(&self, period: usize) -> Self {
        let len = self.len();
        let mut sum = Self::empty(len);
        let mut window_sum = 0.0;

        for i in 0..len {
            if let Some(value) = self[i] {
                window_sum += value;

                if i >= period {
                    if let Some(old_value) = self[i - period] {
                        window_sum -= old_value;
                    }
                }

                sum[i] = Some(window_sum);
            }
        }

        sum
    }

    pub fn mean(&self, period: usize) -> Self {
        let len = self.len();
        let mut mean = Self::empty(len);
        let mut window_sum = 0.0;
        let mut count = 0;

        for i in 0..len {
            if let Some(value) = self[i] {
                window_sum += value;
                count += 1;

                if i >= period {
                    if let Some(old_value) = self[i - period] {
                        window_sum -= old_value;
                        count -= 1;
                    }
                }

                if count > 0 {
                    mean[i] = Some(window_sum / count as f64);
                }
            }
        }

        mean
    }

    pub fn std(&self, period: usize) -> Self {
        let len = self.len();
        let mut std = Self::empty(len);
        let mean = self.mean(period);
        let mut window = Vec::with_capacity(period);

        for i in 0..len {
            let value = self[i];

            if let Some(v) = value {
                window.push(v);

                if window.len() > period {
                    window.remove(0);
                }
            }

            let count = window.len();

            if count > 0 {
                let mean_val = mean[i].unwrap_or(0.0);
                let variance =
                    window.iter().map(|&v| (v - mean_val).powi(2)).sum::<f64>() / count as f64;
                std[i] = Some(variance.sqrt());
            }
        }

        std
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
