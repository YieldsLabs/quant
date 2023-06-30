pub fn median_price(high: &[f64], low: &[f64]) -> Vec<Option<f64>> {
    let len = high.len();

    if len != low.len() {
        return vec![None; len];
    }

    high.iter()
        .zip(low)
        .map(|(&h, &l)| Some((h + l) / 2.0))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_median_price() {
        let high = vec![1.0, 2.0, 3.0];
        let low = vec![0.5, 1.0, 2.0];
        let expected = vec![Some(0.75), Some(1.5), Some(2.5)];

        let result = median_price(&high, &low);

        assert_eq!(result, expected);
    }
}
