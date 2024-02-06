use core::prelude::*;

const ZERO: f32 = 0.;
const PERCENTAGE_SCALE: f32 = 100.;

pub fn tii(
    source: &Series<f32>,
    smooth_type: Smooth,
    major_period: usize,
    minor_period: usize,
) -> Series<f32> {
    let price_diff = source - source.smooth(smooth_type, major_period);

    let positive_sum = price_diff.max(&ZERO).smooth(smooth_type, minor_period);
    let negative_sum = price_diff
        .min(&ZERO)
        .abs()
        .smooth(smooth_type, minor_period);

    PERCENTAGE_SCALE * &positive_sum / (positive_sum + negative_sum)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tii() {
        let source = Series::from([
            6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365, 6.8310, 6.8355,
            6.8360, 6.8345, 6.8285, 6.8395,
        ]);
        let major_period = 4;
        let minor_period = 2;
        let expected = vec![
            0.0, 100.0, 11.999313, 18.140203, 100.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 45.4577,
            100.0, 4.648687, 48.748272,
        ];

        let result: Vec<f32> = tii(&source, Smooth::SMA, major_period, minor_period).into();

        assert_eq!(result, expected);
    }
}
