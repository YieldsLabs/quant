use core::series::Series;

pub fn sma(source: &[f64], period: usize) -> Series<f64> {
    let source = Series::from(source);

    let sma = source.ma(period);

    sma
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![1.0, 1.5, 2.0, 3.0, 4.0];

        let result: Vec<f64> = sma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
