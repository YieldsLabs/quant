use crate::stoch;
use core::prelude::*;

pub fn sso(
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
    smooth_type: Smooth,
    period: usize,
) -> Series<f32> {
    let high_smooth = high.smooth(smooth_type, period);
    let low_smooth = low.smooth(smooth_type, period);
    let close_smooth = close.smooth(smooth_type, period);

    let k = stoch(&close_smooth, &high_smooth, &low_smooth, period);

    k.nz(Some(50.))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sso() {
        let high = Series::from([3.0, 3.0, 3.0, 3.0, 3.0]);
        let low = Series::from([1.0, 1.0, 1.0, 1.0, 1.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let period = 3;

        let expected_k = vec![50.0, 50.0, 58.333336, 41.666668, 41.666668];

        let k = sso(&high, &low, &close, Smooth::WMA, period);

        let result_k: Vec<f32> = k.into();

        assert_eq!(result_k, expected_k);
    }
}
