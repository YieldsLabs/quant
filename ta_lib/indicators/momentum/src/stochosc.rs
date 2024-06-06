use crate::stoch;
use core::prelude::*;

pub fn stochosc(
    source: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    smooth_type: Smooth,
    period: usize,
    k_period: usize,
    d_period: usize,
) -> (Series<f32>, Series<f32>) {
    let stoch = stoch(source, high, low, period);

    let k = stoch.smooth(smooth_type, k_period);

    let d = k.smooth(smooth_type, d_period);

    (k, d)
}

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
    fn test_stochosc() {
        let high = Series::from([3.0, 3.0, 3.0, 3.0, 3.0]);
        let low = Series::from([1.0, 1.0, 1.0, 1.0, 1.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let period = 3;
        let k_period = 3;
        let d_period = 3;
        let epsilon = 0.0001;

        let expected_k = [50.0, 62.5, 58.3333, 50.0, 41.6666];
        let expected_d = [50.0, 56.25, 56.9444, 56.9444, 50.0];

        let (k, d) = stochosc(&close, &high, &low, Smooth::SMA, period, k_period, d_period);

        let result_k: Vec<f32> = k.into();
        let result_d: Vec<f32> = d.into();

        for i in 0..result_k.len() {
            assert!(
                (result_k[i] - expected_k[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                result_k[i],
                expected_k[i]
            );
            assert!(
                (result_d[i] - expected_d[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                result_d[i],
                expected_d[i]
            );
        }
    }

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
