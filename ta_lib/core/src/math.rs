use crate::series::Series;
use crate::{NEUTRALITY, SCALE, ZERO};
use std::ops::Neg;

impl Series<f32> {
    pub fn abs(&self) -> Self {
        self.fmap(|val| val.map(|v| v.abs()))
    }

    pub fn log(&self) -> Self {
        self.fmap(|val| val.filter(|&v| v > &ZERO).map(|v| v.ln()))
    }

    pub fn log10(&self) -> Self {
        self.fmap(|val| val.filter(|&v| v > &ZERO).map(|v| v.log10()))
    }

    pub fn exp(&self) -> Self {
        self.fmap(|val| val.map(|v| v.exp()))
    }

    pub fn pow(&self, period: usize) -> Self {
        self.fmap(|val| val.map(|v| v.powi(period as i32)))
    }

    pub fn sign(&self) -> Self {
        self.fmap(|val| val.map(|v| v.signum()))
    }

    pub fn negate(&self) -> Self {
        self.fmap(|val| val.map(|v| v.neg()))
    }

    pub fn sqrt(&self) -> Self {
        self.fmap(|val| val.filter(|&v| v >= &ZERO).map(|v| v.sqrt()))
    }

    pub fn round(&self, places: usize) -> Self {
        let multiplier = 10.0_f32.powi(places as i32);
        self.fmap(|val| val.map(|v| (v * multiplier).round() / multiplier))
    }

    pub fn cumsum(&self) -> Self {
        let mut sum = ZERO;

        self.fmap(|val| {
            val.map(|v| {
                sum += v;
                sum
            })
        })
    }
}

impl Series<f32> {
    fn all_none(window: &[Option<f32>]) -> bool {
        window.iter().all(|&x| x.is_none())
    }

    fn wsum(&self, window: &[Option<f32>]) -> Option<f32> {
        if Self::all_none(window) {
            return None;
        }

        Some(window.iter().flatten().sum())
    }

    fn wmean(&self, window: &[Option<f32>]) -> Option<f32> {
        self.wsum(window).map(|sum| sum / window.len() as f32)
    }

    fn wpercentile(&self, window: &[Option<f32>], percentile: f32) -> Option<f32> {
        if Self::all_none(window) {
            return None;
        }

        let mut values: Vec<f32> = window.iter().flatten().copied().collect();
        values.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));

        let len = values.len();
        let idx = (percentile / SCALE) * (len as f32 - 1.0);
        let idx_lower = idx.floor() as usize;
        let idx_upper = idx.ceil() as usize;

        if idx_upper >= len {
            Some(values[len - 1]);
        }

        let value_lower = values[idx_lower];
        let value_upper = values[idx_upper];

        if idx_lower == idx_upper {
            Some(values[idx_lower]);
        }

        let fraction = idx.fract();

        Some(value_lower + fraction * (value_upper - value_lower))
    }

    pub fn sum(&self, period: usize) -> Self {
        self.window(period).map(|w| self.wsum(w)).collect()
    }

    pub fn ma(&self, period: usize) -> Self {
        self.window(period).map(|w| self.wmean(w)).collect()
    }

    pub fn percentile(&self, period: usize, percentage: f32) -> Self {
        self.window(period)
            .map(|w| self.wpercentile(w, percentage))
            .collect()
    }

    pub fn median(&self, period: usize) -> Self {
        self.percentile(period, NEUTRALITY)
    }

    pub fn mad(&self, period: usize) -> Self {
        self.window(period)
            .map(|w| {
                self.wmean(w).map(|mean| {
                    w.iter()
                        .flatten()
                        .map(|value| (value - mean).abs())
                        .sum::<f32>()
                        / w.len() as f32
                })
            })
            .collect()
    }

    pub fn var(&self, period: usize) -> Self {
        self.pow(2).ma(period) - self.ma(period).pow(2)
    }

    pub fn std(&self, period: usize) -> Self {
        self.var(period).sqrt()
    }

    pub fn zscore(&self, period: usize) -> Self {
        (self - self.ma(period)) / self.std(period)
    }

    pub fn slope(&self, period: usize) -> Self {
        self.change(period) / period as f32
    }

    pub fn change(&self, period: usize) -> Self {
        self - self.shift(period)
    }

    pub fn highest(&self, period: usize) -> Self {
        self.window(period)
            .map(|w| {
                w.iter()
                    .flatten()
                    .max_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal))
            })
            .collect()
    }

    pub fn lowest(&self, period: usize) -> Self {
        self.window(period)
            .map(|w| {
                w.iter()
                    .flatten()
                    .min_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal))
            })
            .collect()
    }

    pub fn range(&self, period: usize) -> Self {
        self.highest(period) - self.lowest(period)
    }

    pub fn normalize(&self, period: usize, scale: f32) -> Self {
        let l = self.lowest(period);
        let h = self.highest(period);

        scale * (self - &l) / (h - l)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_abs() {
        let source = Series::from([-1.0, 2.0, -3.0, 4.0, 5.0]);
        let expected = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);

        let result = source.abs();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_sqrt() {
        let source = Series::from([-1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([f32::NAN, std::f32::consts::SQRT_2, 1.7320508, 2.0, 2.236068]);

        let result = source.sqrt();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_log() {
        let source = Series::from([-1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([
            f32::NAN,
            std::f32::consts::LN_2,
            1.0986123,
            1.3862944,
            1.609438,
        ]);

        let result = source.log();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_log10() {
        let source = Series::from([-1.0, 2.0, 0.0, 4.0, 5.0]);
        let expected = Series::from([
            f32::NAN,
            std::f32::consts::LOG10_2,
            f32::NAN,
            0.60206,
            0.69897,
        ]);
        let result = source.log10();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_exp() {
        let source = Series::from([-1.0, 2.0, -3.0, 4.0, 5.0]);
        let expected = Series::from([0.36787945, 7.389056, 0.049787067, 54.59815, 148.41316]);

        let result = source.exp();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_pow() {
        let source = Series::from([-1.0, 2.0, -3.0, 4.0, 5.0]);
        let expected = Series::from([1.0, 4.0, 9.0, 16.0, 25.0]);
        let n = 2;

        let result = source.pow(n);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_sign() {
        let source = Series::from([-1.0, 2.0, -3.0, 4.0, 5.0]);
        let expected = Series::from([-1.0, 1.0, -1.0, 1.0, 1.0]);

        let result = source.sign();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_round() {
        let source = Series::from([-1.2211, 2.2456, -3.5677, 4.0, 5.3334]);
        let expected = Series::from([-1.0, 2.0, -4.0, 4.0, 5.0]);
        let n = 0;

        let result = source.round(n);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_cumsum() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([1.0, 3.0, 6.0, 10.0, 15.0]);

        let result = source.cumsum();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_sum_first_nan() {
        let source = Series::from([f32::NAN, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([f32::NAN, 2.0, 5.0, 9.0, 12.0]);
        let n = 3;

        let result = source.sum(n);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_sum_last_nan() {
        let source = Series::from([1.0, 2.0, f32::NAN, f32::NAN, f32::NAN]);
        let expected = Series::from([1.0, 3.0, 3.0, 2.0, f32::NAN]);
        let n = 3;

        let result = source.sum(n);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_ma() {
        let source = Series::from([f32::NAN, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([f32::NAN, 1.0, 1.6666666, 3.0, 4.0]);

        let result = source.ma(3);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_median() {
        let source = Series::from([3.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([3.0, 2.5, 3.0, 3.0, 4.0]);

        let result = source.median(3);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_std() {
        let source = Series::from([2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0]);
        let expected = Series::from([
            0.0, 1.0, 1.6329, 1.6329, 1.6329, 0.8164, 0.8164, 0.8164, 0.8164, 0.8164, 0.8164,
        ]);
        let period = 3;
        let epsilon = 0.001;

        let result = source.std(period);

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
    fn test_mad() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([0.0, 0.5, 0.6666667, 0.6666667, 0.6666667]);
        let n = 3;

        let result = source.mad(n);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_zscore() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([0.0, 1.0, 1.224745, 1.2247446, 1.2247455]);
        let n = 3;

        let result = source.zscore(n);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_slope() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([f32::NAN, f32::NAN, f32::NAN, 1.0, 1.0]);
        let n = 3;

        let result = source.slope(n);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_range() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([0.0, 1.0, 2.0, 2.0, 2.0]);
        let n = 3;

        let result = source.range(n);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_change() {
        let source = Series::from([
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ]);
        let length = 1;
        let epsilon = 0.001;
        let expected = Series::from([
            f32::NAN,
            -0.25,
            0.0599,
            -0.540,
            0.7199,
            0.5,
            0.2700,
            0.3200,
            0.4200,
        ]);

        let result = source.change(length);

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
    fn test_highest() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let period = 3;

        let result = source.highest(period);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_lowest() {
        let source = Series::from([f32::NAN, 2.0, 3.0, 1.0, 5.0]);
        let expected = Series::from([f32::NAN, 2.0, 2.0, 1.0, 1.0]);
        let period = 3;

        let result = source.lowest(period);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_normalize() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([0.0, 1.0, 1.0, 1.0, 1.0]);
        let n = 3;
        let scale = 1.;

        let result = source.normalize(n, scale);

        assert_eq!(result, expected);
    }
}
