use core::prelude::*;

pub fn kb(
    source: &Series<f32>,
    period: usize,
    factor: f32,
) -> (Series<f32>, Series<f32>, Series<f32>) {
    let middle_band = 0.5 * (source.highest(period) + source.lowest(period));
    let volatility = factor * source.std(period).highest(period);

    let upper_band = &middle_band + &volatility;
    let lower_band = &middle_band - &volatility;

    (upper_band, middle_band, lower_band)
}

pub fn kbp(source: &Series<f32>, period: usize, factor: f32) -> Series<f32> {
    let (upb, _, lb) = kb(source, period, factor);

    (source - &lb) / (upb - lb)
}

pub fn kbw(source: &Series<f32>, period: usize, factor: f32) -> Series<f32> {
    let (upb, mb, lb) = kb(source, period, factor);

    SCALE * (upb - lb) / mb
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kb() {
        let source = Series::from([2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0]);
        let period = 3;
        let factor = 2.0;
        let epsilon = 0.001;
        let expected_upper_band = [
            2.0, 5.0, 7.265986, 9.265986, 11.265986, 12.265986, 12.265986, 9.632993, 8.632993,
            7.632993,
        ];
        let expected_middle_band = [2.0, 3.0, 4.0, 6.0, 8.0, 9.0, 9.0, 8.0, 7.0, 6.0];
        let expected_lower_band = [
            2.0, 1.0, 0.734014, 2.734014, 4.734014, 5.7340136, 5.7340136, 6.367007, 5.367007,
            4.367007,
        ];

        let (upper_band, middle_band, lower_band) = kb(&source, period, factor);

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
    fn test_kbp() {
        let source = Series::from([2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0]);
        let period = 3;
        let factor = 2.0;
        let expected = [
            0.0, 0.75, 0.80618626, 0.80618614, 0.80618614, 0.5, 0.3469068, 0.19381316, 0.19381405,
            0.19381405,
        ];

        let result: Vec<f32> = kbp(&source, period, factor).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_kbw() {
        let source = Series::from([2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0]);
        let period = 3;
        let factor = 2.0;
        let expected = [
            0.0, 133.33333, 163.2993, 108.86625, 81.64969, 72.5775, 72.57743, 40.824745, 46.65699,
            54.433155,
        ];

        let result: Vec<f32> = kbw(&source, period, factor).into();

        assert_eq!(result, expected);
    }
}
