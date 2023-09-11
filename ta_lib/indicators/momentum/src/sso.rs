use core::series::Series;
use utils::stoch;

pub fn sso(high: &[f32], low: &[f32], close: &[f32], period: usize) -> Series<f32> {
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    let high_smoth = high.wma(period);
    let low_smoth = low.wma(period);
    let close_smoth = close.wma(period);

    let k = stoch(&high_smoth, &low_smoth, &close_smoth, period);

    k.nz(Some(50.0))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sso() {
        let high = vec![3.0, 3.0, 3.0, 3.0, 3.0];
        let low = vec![1.0, 1.0, 1.0, 1.0, 1.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];
        let period = 3;

        let expected_k = vec![50.0, 50.0, 58.333336, 41.666668, 41.666668];

        let k = sso(&high, &low, &close, period);

        let result_k: Vec<f32> = k.into();

        assert_eq!(result_k, expected_k);
    }
}
