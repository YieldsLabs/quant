use core::Series;

pub fn apo(source: &Series<f32>, short_period: usize, long_period: usize) -> Series<f32> {
    source.ema(short_period) - source.ema(long_period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_apo() {
        let source = Series::from([3.0, 4.0, 5.0, 6.0, 7.0]);
        let short_period = 2;
        let long_period = 4;
        let expected = vec![0.0, 0.26666665, 0.51555586, 0.6945181, 0.8117728];

        let result: Vec<f32> = apo(&source, short_period, long_period).into();

        assert_eq!(result, expected);
    }
}
