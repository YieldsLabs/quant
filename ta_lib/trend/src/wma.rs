use core::series::Series;

pub fn wma(source: &[f64], period: usize) -> Vec<f64> {
    let source = Series::from(&source);

    let wma = source.wma(period);

    wma.into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_wma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let period = 3;
        let epsilon = 0.001;
        let expected = vec![0.0, 0.0, 2.333333, 3.333333, 4.333333];

        let result = wma(&source, period);

        for i in 0..source.len() {
            assert!(
                (result[i] - expected[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                result[i],
                expected[i]
            )
        }
    }
}
