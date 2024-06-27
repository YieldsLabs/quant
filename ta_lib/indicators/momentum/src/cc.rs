use crate::roc;
use core::prelude::*;

pub fn cc(
    source: &Series<f32>,
    period_fast: usize,
    period_slow: usize,
    smooth: Smooth,
    period_smooth: usize,
) -> Series<f32> {
    (roc(source, period_fast) + roc(source, period_slow)).smooth(smooth, period_smooth)
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
