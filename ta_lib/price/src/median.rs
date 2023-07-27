use core::series::Series;

pub fn median_price(high: &[f64], low: &[f64]) -> Vec<f64> {
    let high = Series::from(high);
    let low = Series::from(low);

    let median_price = (high + low) / 2.0;

    median_price.into()
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
