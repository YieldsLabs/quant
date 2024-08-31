use core::prelude::*;

pub fn dch(high: &Price, low: &Price, period: Period) -> (Price, Price, Price) {
    let upper = high.highest(period);
    let lower = low.lowest(period);

    let middle = HALF * (&upper + &lower);

    (upper, middle, lower)
}

pub fn dchw(high: &Price, low: &Price, period: Period) -> Price {
    let (upb, _, lb) = dch(high, low, period);

    upb - lb
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dch() {
        let high = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let low = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let period = 3;
        let expected_upper = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected_lower = vec![1.0, 1.0, 1.0, 2.0, 3.0];

        let expected_middle = vec![1.0, 1.5, 2.0, 3.0, 4.0];

        let (upper, middle, lower) = dch(&high, &low, period);

        let result_upper: Vec<Scalar> = upper.into();
        let result_lower: Vec<Scalar> = lower.into();
        let result_middle: Vec<Scalar> = middle.into();

        assert_eq!(result_upper, expected_upper);
        assert_eq!(result_lower, expected_lower);
        assert_eq!(result_middle, expected_middle);
    }

    #[test]
    fn test_dchw() {
        let high = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let low = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let period = 3;

        let expected = vec![0.0, 1.0, 2.0, 2.0, 2.0];

        let result: Vec<Scalar> = dchw(&high, &low, period).into();

        assert_eq!(result, expected);
    }
}
