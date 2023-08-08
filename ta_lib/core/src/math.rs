use crate::series::Series;

impl Series<f64> {
    fn ew<F>(&self, period: usize, alpha_fn: F) -> Self
    where
        F: Fn(usize) -> f64,
    {
        let alpha = alpha_fn(period);

        let beta = 1.0 - alpha;

        let mut prev = None;

        self.fmap(|current| {
            let result = if let (Some(curr_val), Some(prev_val)) = (current, prev) {
                Some(alpha * curr_val + beta * prev_val)
            } else {
                current.cloned()
            };

            prev = result;
            result
        })
    }

    pub fn smax(&self, scalar: f64) -> Self {
        self.fmap(|val| val.map(|v| v.max(scalar)).or(Some(scalar)))
    }

    pub fn max(&self, rhs: &Series<f64>) -> Self {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(a_val.max(*b_val)),
            _ => None,
        })
    }

    pub fn smin(&self, scalar: f64) -> Self {
        self.fmap(|val| val.map(|v| v.min(scalar)).or(Some(scalar)))
    }

    pub fn min(&self, rhs: &Series<f64>) -> Self {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(a_val.min(*b_val)),
            _ => None,
        })
    }

    pub fn abs(&self) -> Self {
        self.fmap(|val| val.map(|v| v.abs()))
    }

    pub fn round(&self, places: usize) -> Self {
        let multiplier = 10f64.powi(places as i32);
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

    pub fn wma(&self, period: usize) -> Self {
        let len = self.len();
        let mut wma = Series::empty(len);

        let weight_sum = (period * (period + 1)) as f64 / 2.0;

        let mut sum = 0.0;

        for i in 0..period {
            let weight = (i + 1) as f64;
            sum += self[i].unwrap_or(0.0) * weight;
        }

        wma[period - 1] = Some(sum / weight_sum);

        for i in period..len {
            sum += (self[i].unwrap_or(0.0) - self[i - period].unwrap_or(0.0)) * period as f64
                - (weight_sum - period as f64);
            wma[i] = Some(sum / weight_sum);
        }

        wma
    }

    pub fn var(&self, period: usize) -> Self {
        let ma: Vec<f64> = self.ma(period).into();

        self.sliding_map(period, |window, size, i| {
            let ma_val = ma[i];
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
        self.var(period).fmap(|val| val.map(|v| v.sqrt()))
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
    fn test_ma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![Some(1.0), Some(1.5), Some(2.0), Some(3.0), Some(4.0)];
        let series = Series::from(&source);

        let result = series.ma(3);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_ema() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![Some(1.0), Some(1.5), Some(2.25), Some(3.125), Some(4.0625)];
        let series = Series::from(&source);

        let result = series.ema(3);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_smma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![
            Some(1.0),
            Some(1.3333333333333335),
            Some(1.888888888888889),
            Some(2.5925925925925926),
            Some(3.3950617283950617),
        ];
        let series = Series::from(&source);

        let result = series.smma(3);

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
