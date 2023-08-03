use core::series::Series;

pub fn vo(source: &[f64], short_period: usize, long_period: usize) -> Vec<f64> {
    let source = Series::from(source);

    let vo_short = source.ema(short_period);
    let vo_long = source.ema(long_period);

    let vo = 100.0 * (vo_short - &vo_long) / vo_long;

    vo.into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vo() {
        let source = vec![1.0, 2.0, 3.0, 2.0, 1.0];
        let expected = vec![0.0, 11.1111, 13.5802, 2.83224, -10.71604];
        let epsilon = 0.001;

        let result = vo(&source, 2, 3);

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
