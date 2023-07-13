use core::series::Series;

pub fn average_price(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Vec<f64> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    let average_price = (open + &high + &low + &close) / 4.0;

    average_price.into()
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
        let expected = vec![1.5625, 3.125, 4.6875];

        let result = average_price(&open, &high, &low, &close);

        assert_eq!(result, expected);
    }
}
