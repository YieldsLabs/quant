use core::prelude::*;

pub fn rex(
    source: &Series<f32>,
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    smooth: Smooth,
    period: usize,
) -> Series<f32> {
    let source = 3. * source - (open + high + low);

    source.smooth(smooth, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rex() {
        let source = Series::from([2.0310, 2.0282, 1.9937, 1.9795, 1.9632]);
        let open = Series::from([2.0505, 2.0310, 2.0282, 1.9937, 1.9795]);
        let high = Series::from([2.0507, 2.0310, 2.0299, 1.9977, 1.9824]);
        let low = Series::from([2.0174, 2.0208, 1.9928, 1.9792, 1.9616]);

        let expected = vec![
            -0.025600433,
            -0.011900425,
            -0.040849924,
            -0.036474824,
            -0.035187542,
        ];

        let period = 3;

        let result: Vec<f32> = rex(&source, &open, &high, &low, Smooth::EMA, period).into();

        assert_eq!(result, expected);
    }
}
