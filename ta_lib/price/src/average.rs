use core::prelude::*;

pub fn average_price(open: &Price, high: &Price, low: &Price, close: &Price) -> Price {
    (open + high + low + close) / 4.
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_average_price() {
        let open = Series::from([1.5, 3.0, 4.5]);
        let high = Series::from([2.0, 4.0, 6.0]);
        let low = Series::from([1.0, 2.0, 3.0]);
        let close = Series::from([1.75, 3.5, 5.25]);

        let expected = vec![1.5625, 3.125, 4.6875];

        let result: Vec<Scalar> = average_price(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
