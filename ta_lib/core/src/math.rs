use crate::series::Series;
use crate::smoothing::Smooth;
use crate::ZERO;
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
    fn wsum(&self, window: &[Option<f32>]) -> Option<f32> {
        let sum: f32 = window.iter().flatten().sum();

        if window.iter().all(|&x| x.is_none()) {
            None
        } else {
            Some(sum)
        }
    }

    fn wmean(&self, window: &[Option<f32>]) -> Option<f32> {
        self.wsum(window).map(|sum| sum / window.len() as f32)
    }

    pub fn sum(&self, period: usize) -> Self {
        self.window(period).map(|w| self.wsum(&w)).collect()
    }

    pub fn ma(&self, period: usize) -> Self {
        self.window(period).map(|w| self.wmean(&w)).collect()
    }

    pub fn mad(&self, period: usize) -> Self {
        self.window(period)
            .map(|w| {
                self.wmean(&w).map(|mean| {
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
}
