use core::prelude::*;

pub fn apo(source: &Series<f32>, fast_period: usize, slow_period: usize) -> Series<f32> {
    source.smooth(Smooth::EMA, fast_period) - source.smooth(Smooth::EMA, slow_period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_apo() {
        let source = Series::from([3.0, 4.0, 5.0, 6.0, 7.0]);
        let fast_period = 2;
        let slow_period = 4;
        let expected = vec![0.0, 0.26666665, 0.51555586, 0.6945181, 0.8117728];

        let result: Vec<f32> = apo(&source, fast_period, slow_period).into();

        assert_eq!(result, expected);
    }
}
