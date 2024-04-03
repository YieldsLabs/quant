use crate::roc;
use core::prelude::*;

pub fn cc(
    source: &Series<f32>,
    fast_period: usize,
    slow_period: usize,
    smooth_type: Smooth,
    smoothing_period: usize,
) -> Series<f32> {
    (roc(source, fast_period) + roc(source, slow_period)).smooth(smooth_type, smoothing_period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cc() {
        let close = Series::from([19.299, 19.305, 19.310, 19.316, 19.347, 19.355, 19.386]);
        let expected = vec![0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6957161];

        let result: Vec<f32> = cc(&close, 3, 5, Smooth::WMA, 2).into();

        assert_eq!(result, expected);
    }
}
