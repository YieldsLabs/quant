use overlap::sma::sma;
use utils::stoch::stoch;

pub fn stochosc(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
    k_period: usize,
    d_period: usize,
) -> (Vec<Option<f64>>, Vec<Option<f64>>) {
    let len = high.len();

    if len < period {
        return (vec![None; len], vec![None; len]);
    }

    let stoch_values = stoch(high, low, close, period);

    let stoch_len = stoch_values.len();

    let k_sma = sma(
        &stoch_values.iter().filter_map(|&x| x).collect::<Vec<_>>(),
        k_period,
    );
    let mut k = vec![None; stoch_len - k_sma.len()];
    k.extend(k_sma);

    let d_sma = sma(&k.iter().filter_map(|&x| x).collect::<Vec<_>>(), d_period);
    let mut d = vec![None; stoch_len - d_sma.len()];
    d.extend(d_sma);

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

        let expected_k = vec![None, None, None, None, Some(41.666666666666664)];
        let expected_d = vec![None, None, None, None, None];

        let (result_k, result_d) = stochosc(&high, &low, &close, period, k_period, d_period);

        assert_eq!(result_k, expected_k);
        assert_eq!(result_d, expected_d);
    }
}
