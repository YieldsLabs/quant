use core::prelude::*;

pub fn cci(source: &Price, period: Period, factor: Scalar) -> Price {
    source.ad(period) / (factor * source.mad(period))
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::prelude::*;

    #[test]
    fn test_cci() {
        let high = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let low = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let close = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let hlc3 = typical_price(&high, &low, &close);
        let expected = vec![0.0, 66.66667, 100.0, 100.0, 100.0];

        let result: Vec<Scalar> = cci(&hlc3, 3, 0.015).into();

        assert_eq!(result, expected);
    }
}
