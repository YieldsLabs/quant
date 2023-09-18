use core::series::Series;

pub fn kbands(
    source: &[f32],
    period: usize,
    factor: f32,
) -> (Series<f32>, Series<f32>, Series<f32>) {
    let source = Series::from(source);

    let middle_band = (source.highest(period) + source.lowest(period)) / 2.0;
    let volatility = source.std(period).highest(period) * factor;

    let upper_band = &middle_band + &volatility;
    let lower_band = &middle_band - &volatility;

    (upper_band, middle_band, lower_band)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kbands() {
        let source = vec![2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0];
        let period = 3;
        let factor = 2.0;
        let epsilon = 0.001;
        let expected_upper_band = vec![
            2.0, 5.0, 7.265986, 9.265986, 11.265986, 12.265986, 12.265986, 9.632993, 8.632993,
            7.632993,
        ];
        let expected_middle_band = vec![2.0, 3.0, 4.0, 6.0, 8.0, 9.0, 9.0, 8.0, 7.0, 6.0];
        let expected_lower_band = vec![
            2.0, 1.0, 0.734014, 2.734014, 4.734014, 5.7340136, 5.7340136, 6.367007, 5.367007,
            4.367007,
        ];

        let (upper_band, middle_band, lower_band) = kbands(&source, period, factor);

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