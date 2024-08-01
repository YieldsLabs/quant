use core::prelude::*;

pub fn bb(
    source: &Series<f32>,
    smooth: Smooth,
    period: usize,
    factor: f32,
) -> (Series<f32>, Series<f32>, Series<f32>) {
    let middle_band = source.smooth(smooth, period);
    let volatility = factor * source.std(period);

    let upper_band = &middle_band + &volatility;
    let lower_band = &middle_band - &volatility;

    (upper_band, middle_band, lower_band)
}

pub fn bbp(source: &Series<f32>, smooth: Smooth, period: usize, factor: f32) -> Series<f32> {
    let (upb, _, lb) = bb(source, smooth, period, factor);

    (source - &lb) / (upb - lb)
}

pub fn bbw(source: &Series<f32>, smooth: Smooth, period: usize, factor: f32) -> Series<f32> {
    let (upb, mb, lb) = bb(source, smooth, period, factor);

    SCALE * (upb - lb) / mb
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bb() {
        let source = Series::from([2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0]);
        let period = 3;
        let factor = 2.0;
        let epsilon = 0.001;
        let expected_upper_band = [
            2.0, 5.0, 7.265986, 9.265986, 11.265986, 10.632993, 10.632993, 9.632993, 8.632993,
            7.632993,
        ];
        let expected_middle_band = [2.0, 3.0, 4.0, 6.0, 8.0, 9.0, 9.0, 8.0, 7.0, 6.0];
        let expected_lower_band = [
            2.0, 1.0, 0.734014, 2.734014, 4.734014, 7.367007, 7.367007, 6.367007, 5.367007,
            4.367007,
        ];

        let (upper_band, middle_band, lower_band) = bb(&source, Smooth::SMA, period, factor);

        let result_upper_band: Vec<f32> = upper_band.into();
        let result_middle_band: Vec<f32> = middle_band.into();
        let result_lower_band: Vec<f32> = lower_band.into();

        for i in 0..source.len() {
            let a = result_upper_band[i];
            let b = expected_upper_band[i];
            assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);

            let a = result_middle_band[i];
            let b = expected_middle_band[i];
            assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);

            let a = result_lower_band[i];
            let b = expected_lower_band[i];
            assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);
        }
    }

    #[test]
    fn test_bbp() {
        let source = Series::from([2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0]);
        let period = 3;
        let factor = 2.0;
        let expected = [
            0.0, 0.75, 0.80618626, 0.80618614, 0.8061864, 0.5, 0.19381316, 0.19381316, 0.19381405,
            0.19381405,
        ];
        let result: Vec<f32> = bbp(&source, Smooth::SMA, period, factor).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_bbw() {
        let source = Series::from([2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0]);
        let period = 3;
        let factor = 2.0;
        let expected = [
            0.0, 133.33333, 163.2993, 108.86625, 81.64961, 36.288662, 36.288662, 40.824745,
            46.65699, 54.433155,
        ];
        let result: Vec<f32> = bbw(&source, Smooth::SMA, period, factor).into();

        assert_eq!(result, expected);
    }
}
