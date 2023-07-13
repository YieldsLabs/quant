pub fn median_price(high: &[f64], low: &[f64]) -> Vec<f64> {
    high.iter().zip(low).map(|(&h, &l)| (h + l) / 2.0).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_median_price() {
        let high = vec![1.0, 2.0, 3.0];
        let low = vec![0.5, 1.0, 2.0];
        let expected = vec![0.75, 1.5, 2.5];

        let result = median_price(&high, &low);

        assert_eq!(result, expected);
    }
}
