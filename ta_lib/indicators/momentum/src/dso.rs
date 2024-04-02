use crate::stoch;
use core::prelude::*;

pub fn dso(
    close: &Series<f32>,
    smooth_type: Smooth,
    smooth_period: usize,
    k_period: usize,
    d_period: usize,
) -> (Series<f32>, Series<f32>) {
    let close_smooth = close.smooth(smooth_type, k_period);

    let k = stoch(&close_smooth, &close_smooth, &close_smooth, smooth_period)
        .smooth(smooth_type, k_period);
    let d = k.smooth(smooth_type, d_period);

    (k, d)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dso() {
        let close = Series::from([4.9112, 4.9140, 4.9135, 4.9151, 4.9233, 4.9313, 4.9357]);
        let period = 3;
        let k_period = 2;
        let d_period = 2;

        let expected_k = vec![
            0.0, 66.66667, 88.88889, 96.2963, 98.76544, 99.588486, 99.86283,
        ];
        let expected_d = vec![
            0.0, 44.44445, 74.07408, 88.8889, 95.47326, 98.21674, 99.31413,
        ];

        let (k, d) = dso(&close, Smooth::EMA, period, k_period, d_period);

        let result_k: Vec<f32> = k.into();
        let result_d: Vec<f32> = d.into();

        assert_eq!(result_k, expected_k);
        assert_eq!(result_d, expected_d);
    }
}
