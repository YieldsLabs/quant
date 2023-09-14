use crate::series::Series;

macro_rules! iff {
    ($cond:expr, $if_true:expr, $if_false:expr) => {{
        let data = $cond
            .into_iter()
            .zip($if_true.clone().into_iter())
            .zip($if_false.clone().into_iter())
            .map(|((cond_val, true_val), false_val)| match cond_val {
                Some(true_condition) if true_condition => true_val.unwrap_or(f32::NAN),
                _ => false_val.unwrap_or(f32::NAN),
            })
            .collect::<Vec<_>>();

        Series::from(data)
    }};
}

impl Series<f32> {
    fn ew<F>(&self, period: usize, alpha_fn: F, seed: &Series<f32>) -> Self
    where
        F: Fn(usize) -> f32,
    {
        let alpha = alpha_fn(period);

        let beta = 1.0 - alpha;

        let mut sum = Series::empty(self.len());

        for _ in 0..self.len() {
            sum = iff!(
                sum.shift(1).na(),
                seed,
                alpha * self + beta * &sum.shift(1).nz(Some(0.0))
            )
        }

        sum
    }

    pub fn ma(&self, period: usize) -> Self {
        self.sliding_map(period, |window, size, _| {
            Some(window.iter().filter_map(|v| *v).sum::<f32>() / size as f32)
        })
    }

    pub fn ema(&self, period: usize) -> Self {
        self.ew(period, |period| 2.0 / (period as f32 + 1.0), self)
    }

    pub fn smma(&self, period: usize) -> Self {
        self.ew(period, |period| 1.0 / (period as f32), &self.ma(period))
    }

    pub fn wma(&self, period: usize) -> Self {
        let len = self.len();

        let mut sum = Series::empty(len).nz(Some(0.0));
        let mut norm = 0.0;

        for i in 0..period {
            let weight = (period - i) as f32;

            norm += weight;
            sum = sum + self.shift(i) * weight;
        }

        sum / norm
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
