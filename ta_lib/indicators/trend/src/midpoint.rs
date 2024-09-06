use core::prelude::*;

pub fn midpoint(high: &Price, low: &Price, period: Period) -> Price {
    HALF * (high.highest(period) + low.lowest(period))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_midpoint() {
        let high = Series::from([2.0859, 2.0881, 2.0889, 2.0896, 2.0896, 2.0907]);
        let low = Series::from([2.0846, 2.0846, 2.0881, 2.0886, 2.0865, 2.0875]);
        let expected = vec![2.08525, 2.08635, 2.08675, 2.0871, 2.08805, 2.0886];

        let result: Vec<Scalar> = midpoint(&high, &low, 3).into();

        assert_eq!(result, expected);
    }
}
