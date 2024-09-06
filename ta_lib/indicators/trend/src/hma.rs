use core::prelude::*;

pub fn hma(source: &Price, period: Period) -> Price {
    source.smooth(Smooth::HMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hma() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = vec![1.0, 2.3333335, 3.6666667, 4.666667, 5.6666665];

        let result: Vec<Scalar> = hma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
