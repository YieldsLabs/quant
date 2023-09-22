use core::Series;
use utils::stoch;

pub fn stochosc(
    high: &[f32],
    low: &[f32],
    close: &[f32],
    period: usize,
    k_period: usize,
    d_period: usize,
) -> (Series<f32>, Series<f32>) {
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    let stoch = stoch(&high, &low, &close, period);

    let k = stoch.ma(k_period);

    let d = k.ma(d_period);

    (k, d)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stochosc() {
        let high = vec![3.0, 3.0, 3.0, 3.0, 3.0];
        let low = vec![1.0, 1.0, 1.0, 1.0, 1.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];
        let period = 3;
        let k_period = 3;
        let d_period = 3;
        let epsilon = 0.0001;

        let expected_k = [50.0, 62.5, 58.3333, 50.0, 41.6666];
        let expected_d = [50.0, 56.25, 56.9444, 56.9444, 50.0];

        let (k, d) = stochosc(&high, &low, &close, period, k_period, d_period);

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
}
