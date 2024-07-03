use core::prelude::*;

pub fn stc(
    source: &Series<f32>,
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
    cycle: usize,
    d_first: usize,
    d_second: usize,
) -> Series<f32> {
    source
        .spread(smooth_type, fast_period, slow_period)
        .normalize(cycle, SCALE)
        .smooth(smooth_type, d_first)
        .normalize(cycle, SCALE)
        .smooth(smooth_type, d_second)
        .clip(&ZERO, &SCALE)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stc() {
        let source = Series::from([
            1.3626, 1.3630, 1.3637, 1.3653, 1.3692, 1.3689, 1.3719, 1.3715, 1.3732, 1.3701, 1.3730,
            1.3742,
        ]);
        let fast_period = 2;
        let slow_period = 3;
        let cycle = 2;
        let d_first = 3;
        let d_second = 3;
        let expected = vec![
            0.0, 50.0, 75.0, 87.5, 93.75, 46.875, 73.4375, 36.71875, 68.359375, 34.179688,
            67.08984, 83.54492,
        ];

        let result: Vec<f32> = stc(
            &source,
            Smooth::EMA,
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        )
        .into();

        assert_eq!(result, expected);
    }
}
