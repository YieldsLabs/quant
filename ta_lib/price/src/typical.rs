pub fn typical_price(high: &[f64], low: &[f64], close: &[f64]) -> Vec<Option<f64>> {
    let len = high.len();

    if len != low.len() || len != close.len() {
        return vec![None; len];
    }

    high.iter()
        .zip(low)
        .zip(close)
        .map(|((&h, &l), &c)| Some((h + l + c) / 3.0))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_typical_price() {
        let high = vec![1.0, 2.0, 3.0];
        let low = vec![0.5, 1.0, 1.5];
        let close = vec![0.75, 1.5, 2.25];

        let expected = vec![Some(0.75), Some(1.5), Some(2.25)];
        let result = typical_price(&high, &low, &close);

        assert_eq!(result, expected);
    }
}
