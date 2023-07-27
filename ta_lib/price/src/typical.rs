use core::series::Series;

pub fn typical_price(high: &[f64], low: &[f64], close: &[f64]) -> Vec<f64> {
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    let typical_price = (high + low + close) / 3.0;

    typical_price.into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_typical_price() {
        let high = vec![1.0, 2.0, 3.0];
        let low = vec![0.5, 1.0, 1.5];
        let close = vec![0.75, 1.5, 2.25];
        let expected = vec![0.75, 1.5, 2.25];

        let result = typical_price(&high, &low, &close);

        assert_eq!(result, expected);
    }
}
