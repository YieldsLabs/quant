use core::prelude::*;

pub fn tii(source: &Price, smooth: Smooth, period_major: Period, period_minor: Period) -> Price {
    let price_diff = source - source.smooth(smooth, period_major);

    let positive_sum = price_diff.max(&ZERO).smooth(smooth, period_minor);
    let negative_sum = price_diff.min(&ZERO).abs().smooth(smooth, period_minor);

    SCALE * &positive_sum / (positive_sum + negative_sum)
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
