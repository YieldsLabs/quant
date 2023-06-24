pub fn average_price(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Vec<Option<f64>> {
    let len = high.len();

    if len != low.len() || len != open.len() || len != close.len() {
        return vec![None; len];
    }

    high.iter()
        .zip(low)
        .zip(open)
        .zip(close)
        .map(|(((&h, &l), &o), &c)| Some((h + l + o + c) / 4.0))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_average_price() {
        let open = vec![1.5, 3.0, 4.5];
        let high = vec![2.0, 4.0, 6.0];
        let low = vec![1.0, 2.0, 3.0];
        let close = vec![1.75, 3.5, 5.25];

        let expected = vec![Some(1.5625), Some(3.125), Some(4.6875)];
        let result = average_price(&open, &high, &low, &close);

        assert_eq!(result, expected);
    }
}
