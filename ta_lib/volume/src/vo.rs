use core::series::Series;
use overlap::ema::ema;

pub fn vo(source: &[f64], short_period: usize, long_period: usize) -> Series<f64> {
    let vo_short = ema(source, short_period);
    let vo_long = ema(source, long_period);

    let vo = 100.0 * (vo_short - &vo_long) / &vo_long;

    vo
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vo() {
        let source = vec![1.0, 2.0, 3.0, 2.0, 1.0];
        let expected = vec![
            Some(0.0),
            Some(11.1111),
            Some(13.5802),
            Some(2.83224),
            Some(-10.71604),
        ];
        let epsilon = 0.001;

        let result = vo(&source, 2, 3);

        for i in 0..source.len() {
            match (result[i], expected[i]) {
                (Some(a), Some(b)) => {
                    assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b)
                }
                (None, None) => {}
                _ => panic!("at position {}: {:?} != {:?}", i, result[i], expected[i]),
            }
        }
    }
}
