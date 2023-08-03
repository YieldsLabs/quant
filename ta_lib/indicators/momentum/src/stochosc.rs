use utils::stoch::stoch;

pub fn stochosc(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
    k_period: usize,
    d_period: usize,
) -> (Vec<f64>, Vec<f64>) {
    let stoch = stoch(high, low, close, period);

    let k = stoch.ma(k_period);

    let d = k.ma(d_period);

    (k.into(), d.into())
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

        let expected_k = vec![50.0, 62.5, 58.3333, 50.0, 41.6666];
        let expected_d = vec![50.0, 56.25, 56.9444, 56.9444, 50.0];

        let (result_k, result_d) = stochosc(&high, &low, &close, period, k_period, d_period);

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
