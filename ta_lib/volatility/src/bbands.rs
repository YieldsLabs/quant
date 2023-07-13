use core::series::Series;

pub fn bbands(
    source: &[f64],
    period: usize,
    factor: f64,
) -> (Series<f64>, Series<f64>, Series<f64>) {
    let source = Series::from(source);

    let middle_band = source.mean(period);
    let std = source.std(period);

    let upper_band = &middle_band + &(factor * &std);
    let lower_band = &middle_band - &(factor * &std);

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
        let expected_upper_band = vec![
            Some(2.0),
            Some(5.0),
            Some(7.265986),
            Some(9.265986),
            Some(11.265986),
            Some(10.632993),
            Some(10.632993),
            Some(9.632993),
            Some(8.632993),
            Some(7.632993),
        ];
        let expected_middle_band = vec![
            Some(2.0),
            Some(3.0),
            Some(4.0),
            Some(6.0),
            Some(8.0),
            Some(9.0),
            Some(9.0),
            Some(8.0),
            Some(7.0),
            Some(6.0),
        ];
        let expected_lower_band = vec![
            Some(2.0),
            Some(1.0),
            Some(0.734014),
            Some(2.734014),
            Some(4.734014),
            Some(7.367007),
            Some(7.367007),
            Some(6.367007),
            Some(5.367007),
            Some(4.367007),
        ];

        let (upper_band, middle_band, lower_band) = bbands(&source, period, factor);

        for i in 0..source.len() {
            match (upper_band[i], expected_upper_band[i]) {
                (Some(a), Some(b)) => {
                    assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b)
                }
                (None, None) => {}
                _ => panic!(
                    "at position {}: {:?} != {:?}",
                    i, upper_band[i], expected_upper_band[i]
                ),
            }

            match (middle_band[i], expected_middle_band[i]) {
                (Some(a), Some(b)) => {
                    assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b)
                }
                (None, None) => {}
                _ => panic!(
                    "at position {}: {:?} != {:?}",
                    i, middle_band[i], expected_middle_band[i]
                ),
            }

            match (lower_band[i], expected_lower_band[i]) {
                (Some(a), Some(b)) => {
                    assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b)
                }
                (None, None) => {}
                _ => panic!(
                    "at position {}: {:?} != {:?}",
                    i, lower_band[i], expected_lower_band[i]
                ),
            }
        }
    }
}
