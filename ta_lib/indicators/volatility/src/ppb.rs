use core::prelude::*;

pub fn ppb(
    source: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    smooth: Smooth,
    period: usize,
    factor: f32,
) -> (Series<f32>, Series<f32>, Series<f32>) {
    let ppvih = factor * high.std(period).highest(period);
    let ppvil = factor * low.std(period).lowest(period);

    let middle = source.smooth(smooth, period);

    let upper = &middle + ppvih;
    let lower = &middle - ppvil;

    (upper, middle, lower)
}

pub fn ppbp(
    source: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    smooth: Smooth,
    period: usize,
    factor: f32,
) -> Series<f32> {
    let (upb, _, lb) = ppb(source, high, low, smooth, period, factor);

    (source - &lb) / (upb - lb)
}

pub fn ppbw(
    source: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    smooth: Smooth,
    period: usize,
    factor: f32,
) -> Series<f32> {
    let (upb, mb, lb) = ppb(source, high, low, smooth, period, factor);

    SCALE * (upb - lb) / mb
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ppb() {
        let source = Series::from([
            19.102, 19.100, 19.146, 19.181, 19.155, 19.248, 19.309, 19.355, 19.439,
        ]);
        let high = Series::from([
            19.129, 19.116, 19.154, 19.195, 19.217, 19.285, 19.341, 19.394, 19.450,
        ]);
        let low = Series::from([
            19.090, 19.086, 19.074, 19.145, 19.141, 19.155, 19.219, 19.306, 19.355,
        ]);
        let factor = 2.0;
        let period = 3;
        let epsilon = 0.0001;
        let expected_upper_band = [
            19.102, 19.116625, 19.149145, 19.207697, 19.22603, 19.27279, 19.338594, 19.405262,
            19.468927,
        ];
        let expected_middle_band = [
            19.102, 19.101, 19.116, 19.142332, 19.160666, 19.194666, 19.237333, 19.304, 19.367666,
        ];
        let expected_lower_band = [
            19.102, 19.101, 19.116, 19.131283, 19.149616, 19.194666, 19.237333, 19.304, 19.299559,
        ];

        let (upper_band, middle_band, lower_band) =
            ppb(&source, &high, &low, Smooth::SMA, period, factor);

        let result_upper_band: Vec<f32> = upper_band.into();
        let result_middle_band: Vec<f32> = middle_band.into();
        let result_lower_band: Vec<f32> = lower_band.into();

        for i in 0..high.len() {
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
    fn test_ppbp() {
        let source = Series::from([
            19.102, 19.100, 19.146, 19.181, 19.155, 19.248, 19.309, 19.355, 19.439,
        ]);
        let high = Series::from([
            19.129, 19.116, 19.154, 19.195, 19.217, 19.285, 19.341, 19.394, 19.450,
        ]);
        let low = Series::from([
            19.090, 19.086, 19.074, 19.145, 19.141, 19.155, 19.219, 19.306, 19.355,
        ]);
        let factor = 2.0;
        let period = 3;
        let expected = [
            0.0,
            -0.063964844,
            0.9051099,
            0.6506003,
            0.070439056,
            0.682666,
            0.70774156,
            0.5036542,
            0.8232956,
        ];

        let result: Vec<f32> = ppbp(&source, &high, &low, Smooth::SMA, period, factor).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_ppbw() {
        let source = Series::from([
            19.102, 19.100, 19.146, 19.181, 19.155, 19.248, 19.309, 19.355, 19.439,
        ]);
        let high = Series::from([
            19.129, 19.116, 19.154, 19.195, 19.217, 19.285, 19.341, 19.394, 19.450,
        ]);
        let low = Series::from([
            19.090, 19.086, 19.074, 19.145, 19.141, 19.155, 19.219, 19.306, 19.355,
        ]);
        let factor = 2.0;
        let period = 3;
        let expected = [
            0.0, 0.081802, 0.17339352, 0.39918908, 0.39880714, 0.40701413, 0.5263783, 0.52456045,
            0.8744923,
        ];

        let result: Vec<f32> = ppbw(&source, &high, &low, Smooth::SMA, period, factor).into();

        assert_eq!(result, expected);
    }
}
