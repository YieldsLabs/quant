use core::series::Series;

pub fn vo(source: &[f32], short_period: usize, long_period: usize) -> Series<f32> {
    let source = Series::from(source);

    let vo_short = source.ema(short_period);
    let vo_long = source.ema(long_period);

    100.0 * (vo_short - &vo_long) / vo_long
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vo() {
        let source = vec![1.0, 2.0, 3.0, 2.0, 1.0];
        let expected = [0.0, 11.1111, 13.5802, 2.83224, -10.71604];
        let epsilon = 0.001;

        let result: Vec<f32> = vo(&source, 2, 3).into();

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
