use crate::iff;
use crate::series::Series;

impl Series<f32> {
    pub fn ew(&self, alpha: &Series<f32>, seed: &Series<f32>) -> Self {
        let mut sum = Series::empty(self.len());

        for _ in 0..self.len() {
            let shifted = sum.shift(1);

            sum = iff!(shifted.na(), seed, alpha * self + (1.0 - alpha) * &shifted)
        }

        sum
    }

    pub fn ma(&self, period: usize) -> Self {
        self.sliding_map(period, |window, size, _| {
            Some(window.iter().filter_map(|v| *v).sum::<f32>() / size as f32)
        })
    }

    pub fn ema(&self, period: usize) -> Self {
        let alpha = Series::fill(self.len(), 2.0 / (period as f32 + 1.0));

        self.ew(&alpha, self)
    }

    pub fn smma(&self, period: usize) -> Self {
        let alpha = Series::fill(self.len(), 1.0 / (period as f32));

        self.ew(&alpha, &self.ma(period))
    }

    pub fn wma(&self, period: usize) -> Self {
        let len = self.len();

        let mut sum = Series::zero(self.len());
        let mut norm = 0.0;

        for i in 0..period {
            let weight = (period - i) as f32;

            norm += weight;
            sum = sum + self.shift(i) * weight;
        }

        sum / norm
    }

    pub fn hma(&self, period: usize) -> Self {
        let lag = (period as f32 / 2.0).round() as usize;
        let sqrt_period = (period as f32).sqrt() as usize;

        (2.0 * self.wma(lag) - self.wma(period)).wma(sqrt_period)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

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
            Some(1.3333333),
            Some(1.8888888),
            Some(2.5925925),
            Some(3.3950615),
        ];
        let series = Series::from(&source);

        let result = series.smma(3);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_wma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![
            None,
            None,
            Some(2.3333333),
            Some(3.3333333),
            Some(4.3333335),
        ];
        let series = Series::from(&source);

        let result = series.wma(3);

        assert_eq!(result, expected);
    }
}
