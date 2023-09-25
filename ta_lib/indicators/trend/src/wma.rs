use core::Series;

pub fn wma(source: &Series<f32>, period: usize) -> Series<f32> {
    source.wma(period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_wma() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let period = 3;
        let epsilon = 0.001;
        let expected = [0.0, 0.0, 2.333333, 3.333333, 4.333333];

        let result: Vec<f32> = wma(&source, period).into();

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
