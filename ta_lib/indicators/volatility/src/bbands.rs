use core::series::Series;

pub fn bbands(
    source: &[f32],
    period: usize,
    factor: f32,
) -> (Series<f32>, Series<f32>, Series<f32>) {
    let source = Series::from(source);

    let middle_band = source.ma(period);
    let std_mul = source.std(period) * factor;

    let upper_band = &middle_band + &std_mul;
    let lower_band = &middle_band - &std_mul;

    (upper_band, middle_band, lower_band)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bbands() {
        let source = vec![2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0];
        let period = 3;
        let factor = 2.0;
        let epsilon = 0.001;
        let expected_upper_band = [2.0, 5.0, 7.265986, 9.265986, 11.265986, 10.632993, 10.632993, 9.632993, 8.632993,
            7.632993];
        let expected_middle_band = [2.0, 3.0, 4.0, 6.0, 8.0, 9.0, 9.0, 8.0, 7.0, 6.0];
        let expected_lower_band = [2.0, 1.0, 0.734014, 2.734014, 4.734014, 7.367007, 7.367007, 6.367007, 5.367007,
            4.367007];

        let (upper_band, middle_band, lower_band) = bbands(&source, period, factor);

        let result_upper_band: Vec<f32> = upper_band.into();
        let result_middle_band: Vec<f32> = middle_band.into();
        let result_lower_band: Vec<f32> = lower_band.into();

        for i in 0..source.len() {
            let a = result_upper_band[i];
            let b = expected_upper_band[i];
            assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);

            let a = result_middle_band[i];
            let b = expected_middle_band[i];
            assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);

            let a = result_lower_band[i];
            let b = expected_lower_band[i];
            assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);
        }
    }
}
