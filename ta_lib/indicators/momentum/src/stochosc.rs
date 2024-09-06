use core::prelude::*;

pub fn stoch(source: &Price, high: &Price, low: &Price, period: Period) -> Price {
    let hh = high.highest(period);
    let ll = low.lowest(period);

    SCALE * (source - &ll) / (hh - ll)
}

pub fn stochosc(
    source: &Price,
    high: &Price,
    low: &Price,
    smooth: Smooth,
    period: Period,
    period_k: Period,
    period_d: Period,
) -> (Price, Price) {
    let k = stoch(source, high, low, period).smooth(smooth, period_k);
    let d = k.smooth(smooth, period_d);

    (k, d)
}

pub fn sso(
    source: &Price,
    high: &Price,
    low: &Price,
    smooth: Smooth,
    period_k: Period,
    period_d: Period,
) -> (Price, Price) {
    let high_smooth = high.smooth(smooth, period_k);
    let low_smooth = low.smooth(smooth, period_k);
    let source = source.smooth(smooth, period_k);

    let k = stoch(&source, &high_smooth, &low_smooth, period_k);
    let d = k.smooth(smooth, period_d);

    (k, d)
}

pub fn dso(
    source: &Price,
    smooth: Smooth,
    period: Period,
    period_k: Period,
    period_d: Period,
) -> (Price, Price) {
    let source = source.smooth(smooth, period_k);

    let k = source.normalize(period, SCALE).smooth(smooth, period_k);
    let d = k.smooth(smooth, period_d);

    (k, d)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stoch() {
        let high = Series::from([3.0, 3.0, 3.0, 3.0, 3.0]);
        let low = Series::from([1.0, 1.0, 1.0, 1.0, 1.0]);
        let source = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let period = 3;

        let expected = vec![50.0, 75.0, 50.0, 25.0, 50.0];

        let result: Vec<Scalar> = stoch(&source, &high, &low, period).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_stochosc() {
        let high = Series::from([3.0, 3.0, 3.0, 3.0, 3.0]);
        let low = Series::from([1.0, 1.0, 1.0, 1.0, 1.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let period = 3;
        let k_period = 3;
        let d_period = 3;
        let epsilon = 0.0001;

        let expected_k = [50.0, 62.5, 58.3333, 50.0, 41.6666];
        let expected_d = [50.0, 56.25, 56.9444, 56.9444, 50.0];

        let (k, d) = stochosc(&close, &high, &low, Smooth::SMA, period, k_period, d_period);

        let result_k: Vec<Scalar> = k.into();
        let result_d: Vec<Scalar> = d.into();

        for i in 0..result_k.len() {
            assert!(
                (result_k[i] - expected_k[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                result_k[i],
                expected_k[i]
            );
            assert!(
                (result_d[i] - expected_d[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                result_d[i],
                expected_d[i]
            );
        }
    }

    #[test]
    fn test_sso() {
        let high = Series::from([3.0, 3.0, 3.0, 3.0, 3.0]);
        let low = Series::from([1.0, 1.0, 1.0, 1.0, 1.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let k_period = 3;
        let d_period = 3;

        let expected_k = vec![50.0, 66.666664, 58.333336, 41.666668, 41.666668];
        let expected_d = vec![50.0, 61.11111, 59.722218, 51.38889, 44.444447];

        let (k, d) = sso(&close, &high, &low, Smooth::WMA, k_period, d_period);

        let result_k: Vec<Scalar> = k.into();
        let result_d: Vec<Scalar> = d.into();

        assert_eq!(result_k, expected_k);
        assert_eq!(result_d, expected_d);
    }

    #[test]
    fn test_dso() {
        let close = Series::from([4.9112, 4.9140, 4.9135, 4.9151, 4.9233, 4.9313, 4.9357]);
        let period = 3;
        let k_period = 2;
        let d_period = 2;

        let expected_k = vec![
            0.0, 66.66667, 88.88889, 96.2963, 98.76544, 99.588486, 99.86283,
        ];
        let expected_d = vec![
            0.0, 44.44445, 74.07408, 88.8889, 95.47326, 98.21674, 99.31413,
        ];

        let (k, d) = dso(&close, Smooth::EMA, period, k_period, d_period);

        let result_k: Vec<Scalar> = k.into();
        let result_d: Vec<Scalar> = d.into();

        assert_eq!(result_k, expected_k);
        assert_eq!(result_d, expected_d);
    }
}
