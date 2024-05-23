use core::prelude::*;

pub fn ppo(
    source: &Series<f32>,
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
) -> Series<f32> {
    let fast = source.smooth(smooth_type, fast_period);
    let slow = source.smooth(smooth_type, slow_period);

    SCALE * (fast - &slow) / &slow
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ppo() {
        let source = Series::from([
            2.0846, 2.0881, 2.0889, 2.0896, 2.0875, 2.0904, 2.0909, 2.0936,
        ]);
        let expected = vec![
            0.0,
            0.027963202,
            0.029670628,
            0.025649877,
            -0.000331128,
            0.018578414,
            0.019517785,
            0.034671485,
        ];
        let fast_period = 2;
        let slow_period = 3;

        let result: Vec<f32> = ppo(&source, Smooth::EMA, fast_period, slow_period).into();

        assert_eq!(result, expected);
    }
}
