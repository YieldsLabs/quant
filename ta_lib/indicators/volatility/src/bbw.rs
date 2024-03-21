use core::prelude::*;

pub fn bbw(source: &Series<f32>, smooth_type: Smooth, period: usize, factor: f32) -> Series<f32> {
    let middle_band = source.smooth(smooth_type, period);
    let std_mul = source.std(period) * factor;

    let upper_band = &middle_band + &std_mul;
    let lower_band = &middle_band - &std_mul;

    (upper_band - lower_band) / &middle_band
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bbw() {
        let source = Series::from([2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0]);
        let period = 3;
        let factor = 2.0;
        let epsilon = 0.001;
        let expected = [
            0.0, 1.3333334, 1.632993, 1.0886625, 0.81649613, 0.36288664, 0.36288664, 0.40824747,
            0.4665699, 0.54433155,
        ];
        let result: Vec<f32> = bbw(&source, Smooth::SMA, period, factor).into();

        assert_eq!(result, expected);
    }
}
