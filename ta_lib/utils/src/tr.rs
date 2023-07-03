pub fn true_range(high: &[f64], low: &[f64], close: &[f64]) -> Vec<f64> {
    let len = high.len();

    if len != low.len() || len != close.len() {
        return vec![0.0; len];
    }

    let mut true_range = vec![0.0; len];

    for i in 1..len {
        let tr = if close[i - 1].is_nan() {
            high[i] - low[i]
        } else {
            f64::max(
                f64::max(high[i] - low[i], f64::abs(high[i] - close[i - 1])),
                f64::abs(low[i] - close[i - 1]),
            )
        };

        true_range[i] = tr;
    }

    true_range
}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_true_range() {
        let high = vec![50.0, 60.0, 55.0, 70.0];
        let low = vec![40.0, 50.0, 45.0, 60.0];
        let close = vec![45.0, 55.0, 50.0, 65.0];
        let expected = vec![0.0, 15.0, 10.0, 20.0];

        let result = true_range(&high, &low, &close);

        assert_eq!(result, expected);
    }
}
