use core::series::Series;

pub fn sma(source: &[f64], period: usize) -> Series<f64> {
    let source = Series::from(source);

    let sma = source.mean(period);

    sma
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![Some(1.0), Some(1.5), Some(2.0), Some(3.0), Some(4.0)];

        let result = sma(&source, 3);

        assert_eq!(result, expected);
    }
}
