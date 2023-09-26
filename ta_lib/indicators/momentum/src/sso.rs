use crate::stoch;
use core::Series;

pub fn sso(
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
    period: usize,
    smoothing: Option<&str>,
) -> Series<f32> {
    let smooth_series = |series: &Series<f32>| -> Series<f32> {
        match smoothing {
            Some("WMA") => series.wma(period),
            Some("HMA") => series.hma(period),
            Some("SMA") | _ => series.ma(period),
        }
    };

    let high_smooth = smooth_series(&high);
    let low_smooth = smooth_series(&low);
    let close_smooth = smooth_series(&close);

    let k = stoch(&high_smooth, &low_smooth, &close_smooth, period);

    k.nz(Some(50.0))
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

        let k = sso(&high, &low, &close, period, Some("WMA"));

        let result_k: Vec<f32> = k.into();

        assert_eq!(result_k, expected_k);
    }
}
