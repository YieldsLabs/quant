pub fn wcl(high: &[f64], low: &[f64], close: &[f64]) -> Vec<f64> {
    let len = high.len();

    if len != low.len() || len != close.len() {
        return vec![0.0; len];
    }

    high.iter()
        .zip(low)
        .zip(close)
        .map(|((&h, &l), &c)| (h + l + (c * 2.0)) / 4.0)
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_weighted_close_price() {
        let high = vec![1.0, 2.0, 3.0];
        let low = vec![0.5, 1.0, 1.5];
        let close = vec![0.75, 1.5, 2.25];
        let expected = vec![0.75, 1.5, 2.25];

        let result = wcl(&high, &low, &close);

        assert_eq!(result, expected);
    }
}
