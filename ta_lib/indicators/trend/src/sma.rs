use core::prelude::*;

pub fn sma(source: &Price, period: Period) -> Price {
    source.smooth(Smooth::SMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sma() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = vec![1.0, 1.5, 2.0, 3.0, 4.0];

        let result: Vec<Scalar> = sma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
