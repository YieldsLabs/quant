use core::prelude::*;

pub fn median_price(high: &Price, low: &Price) -> Price {
    HALF * (high + low)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_median_price() {
        let high = Series::from([1.0, 2.0, 3.0]);
        let low = Series::from([0.5, 1.0, 2.0]);

        let expected = vec![0.75, 1.5, 2.5];

        let result: Vec<Scalar> = median_price(&high, &low).into();

        assert_eq!(result, expected);
    }
}
