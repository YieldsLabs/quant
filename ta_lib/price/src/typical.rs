use core::prelude::*;

pub fn typical_price(high: &Price, low: &Price, close: &Price) -> Price {
    (high + low + close) / 3.
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_typical_price() {
        let high = Series::from([1.0, 2.0, 3.0]);
        let low = Series::from([0.5, 1.0, 1.5]);
        let close = Series::from([0.75, 1.5, 2.25]);

        let expected = vec![0.75, 1.5, 2.25];

        let result: Vec<Scalar> = typical_price(&high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
