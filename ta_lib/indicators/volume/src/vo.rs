use core::prelude::*;

pub fn vo(
    source: &Series<f32>,
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
) -> Series<f32> {
    let vo_fast = source.smooth(smooth_type, fast_period);
    let vo_slow = source.smooth(smooth_type, slow_period);

    SCALE * (vo_fast - &vo_slow) / vo_slow
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vo() {
        let source = Series::from([1.0, 2.0, 3.0, 2.0, 1.0]);
        let expected = [0.0, 11.1111, 13.5802, 2.83224, -10.71604];
        let epsilon = 0.001;

        let result: Vec<f32> = vo(&source, Smooth::EMA, 2, 3).into();

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
