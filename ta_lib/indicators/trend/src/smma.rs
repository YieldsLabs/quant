use core::series::Series;

pub fn smma(source: &[f64], period: usize) -> Series<f64> {
    let source = Series::from(source);

    let smma = source.smma(period);

    smma
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_smma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![1.0, 1.333, 1.888, 2.592, 3.395];
        let epsilon = 0.001;

        let result: Vec<f64> = smma(&source, 3).into();

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
