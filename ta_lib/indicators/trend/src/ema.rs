use core::series::Series;

pub fn ema(source: &[f64], period: usize) -> Vec<f64> {
    let source = Series::from(source);

    let ema = source.ema(period);

    ema.into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ema() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![1.0, 1.5, 2.25, 3.125, 4.0625];

        let result = ema(&source, 3);

        assert_eq!(result, expected);
    }
}
