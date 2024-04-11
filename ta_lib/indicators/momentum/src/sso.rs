use crate::stoch;
use core::prelude::*;

pub fn sso(
    source: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    smooth_type: Smooth,
    k_period: usize,
    d_period: usize,
) -> (Series<f32>, Series<f32>) {
    let high_smooth = high.smooth(smooth_type, k_period);
    let low_smooth = low.smooth(smooth_type, k_period);
    let source = source.smooth(smooth_type, k_period);

    let k = stoch(&source, &high_smooth, &low_smooth, k_period);
    let d = k.smooth(smooth_type, d_period);

    (k, d)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sso() {
        let high = Series::from([3.0, 3.0, 3.0, 3.0, 3.0]);
        let low = Series::from([1.0, 1.0, 1.0, 1.0, 1.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let k_period = 3;
        let d_period = 3;

        let expected_k = vec![0.0, 0.0, 58.333336, 41.666668, 41.666668];
        let expected_d = vec![0.0, 0.0, 0.0, 0.0, 44.444447];

        let (k, d) = sso(&close, &high, &low, Smooth::WMA, k_period, d_period);

        let result_k: Vec<f32> = k.into();
        let result_d: Vec<f32> = d.into();

        assert_eq!(result_k, expected_k);
        assert_eq!(result_d, expected_d);
    }
}
