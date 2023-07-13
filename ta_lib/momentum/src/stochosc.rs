use core::series::Series;
use utils::stoch::stoch;

pub fn stochosc(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
    k_period: usize,
    d_period: usize,
) -> (Series<f64>, Series<f64>) {
    let stoch = stoch(high, low, close, period);

    let k = stoch.mean(k_period);

    let d = k.mean(d_period);

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

        let expected_k = vec![
            Some(50.0),
            Some(62.5),
            Some(58.3333),
            Some(50.0),
            Some(41.6666),
        ];
        let expected_d = vec![
            Some(50.0),
            Some(56.25),
            Some(56.9444),
            Some(56.9444),
            Some(50.0),
        ];

        let (result_k, result_d) = stochosc(&high, &low, &close, period, k_period, d_period);

        for i in 0..result_k.len() {
            match (result_k[i], expected_k[i]) {
                (Some(a), Some(b)) => {
                    assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b)
                }
                (None, None) => {}
                _ => panic!(
                    "at position {}: {:?} != {:?}",
                    i, result_k[i], expected_k[i]
                ),
            }
        }

        for i in 0..result_d.len() {
            match (result_d[i], expected_d[i]) {
                (Some(a), Some(b)) => {
                    assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b)
                }
                (None, None) => {}
                _ => panic!(
                    "at position {}: {:?} != {:?}",
                    i, result_d[i], expected_d[i]
                ),
            }
        }
    }
}
