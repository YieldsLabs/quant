use core::prelude::*;

pub fn supertrend(
    source: &Series<f32>,
    close: &Series<f32>,
    atr: &Series<f32>,
    factor: f32,
) -> (Series<f32>, Series<f32>) {
    let len = source.len();

    let atr_mul = atr * factor;

    let basic_up = source - &atr_mul;
    let mut up = Series::empty(len);

    let basic_dn = source + &atr_mul;
    let mut dn = Series::empty(len);

    let prev_close = close.shift(1);
    let mut direction = Series::empty(len);

    let trend_bull = Series::one(len);
    let trend_bear = trend_bull.negate();

    for _ in 0..len {
        let prev_up = up.shift(1);
        up = iff!(prev_close.sgt(&prev_up), basic_up.max(&prev_up), basic_up);

        let prev_dn = dn.shift(1);
        dn = iff!(prev_close.slt(&prev_dn), basic_dn.min(&prev_dn), basic_dn);

        direction = nz!(direction.shift(1), direction);
        direction = iff!(close.sgte(&prev_dn), trend_bull, direction);
        direction = iff!(close.slte(&prev_up), trend_bear, direction);
    }

    let first_non_empty = direction
        .iter()
        .find(|&&el| el.is_some())
        .map(|&el| -el.unwrap());

    direction = direction.nz(first_non_empty);

    let supertrend = iff!(direction.seq(&ONE), up, dn);

    (direction, supertrend)
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::prelude::*;
    use volatility::atr;

    #[test]
    fn test_supertrend_up_dn() {
        let high = Series::from([
            6.649, 6.644, 6.645, 6.648, 6.644, 6.664, 6.627, 6.633, 6.608, 6.594, 6.593, 6.565,
            6.556, 6.550, 6.561, 6.579, 6.610, 6.615, 6.591, 6.614, 6.637, 6.630,
        ]);
        let low = Series::from([
            6.634, 6.631, 6.632, 6.638, 6.605, 6.623, 6.600, 6.593, 6.578, 6.575, 6.558, 6.536,
            6.536, 6.520, 6.543, 6.559, 6.565, 6.584, 6.581, 6.583, 6.609, 6.608,
        ]);
        let close = Series::from([
            6.644, 6.639, 6.638, 6.644, 6.641, 6.625, 6.624, 6.608, 6.582, 6.592, 6.558, 6.545,
            6.544, 6.546, 6.560, 6.565, 6.610, 6.585, 6.590, 6.609, 6.621, 6.623,
        ]);
        let hl2 = median_price(&high, &low);
        let atr_period = 3;
        let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);

        let factor = 3.0;
        let expected_supertrend = vec![
            6.596499, 6.596499, 6.596833, 6.6052217, 6.6052217, 6.6052217, 6.6052217, 6.6052217,
            6.680167, 6.6658287, 6.664719, 6.6389794, 6.6249866, 6.617658, 6.617658, 6.617658,
            6.617658, 6.617658, 6.617658, 6.617658, 6.5427637, 6.5435085,
        ];
        let expected_direction = vec![
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0,
            -1.0, -1.0, -1.0, -1.0, 1.0, 1.0,
        ];

        let (direction, supertrend) = supertrend(&hl2, &close, &atr, factor);
        let result_direction: Vec<f32> = direction.into();
        let result_supertrend: Vec<f32> = supertrend.into();

        assert_eq!(high.len(), low.len());
        assert_eq!(high.len(), close.len());
        assert_eq!(result_direction, expected_direction);
        assert_eq!(result_supertrend, expected_supertrend);
    }

    #[test]
    fn test_supertrend_dn_up() {
        let high = Series::from([
            6.161, 6.15, 6.157, 6.174, 6.179, 6.192, 6.184, 6.183, 6.185, 6.193, 6.213, 6.201,
            6.205, 6.188, 6.18, 6.194, 6.191, 6.184, 6.194, 6.188, 6.188, 6.195, 6.212, 6.21,
            6.193, 6.178, 6.189, 6.197, 6.205, 6.232, 6.236, 6.222, 6.233, 6.231, 6.224, 6.219,
        ]);
        let low = Series::from([
            6.136, 6.135, 6.143, 6.155, 6.163, 6.17, 6.167, 6.17, 6.161, 6.165, 6.188, 6.183,
            6.186, 6.168, 6.164, 6.176, 6.169, 6.175, 6.176, 6.171, 6.171, 6.182, 6.193, 6.18,
            6.152, 6.161, 6.161, 6.183, 6.189, 6.193, 6.215, 6.205, 6.208, 6.213, 6.196, 6.202,
        ]);
        let close = Series::from([
            6.146, 6.148, 6.155, 6.174, 6.173, 6.172, 6.182, 6.176, 6.167, 6.193, 6.201, 6.198,
            6.188, 6.174, 6.176, 6.191, 6.175, 6.184, 6.188, 6.179, 6.184, 6.195, 6.21, 6.192,
            6.173, 6.174, 6.189, 6.194, 6.202, 6.231, 6.218, 6.208, 6.224, 6.22, 6.208, 6.204,
        ]);
        let hl2 = median_price(&high, &low);
        let atr_period = 3;
        let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);

        let factor = 3.0;
        let expected_supertrend = vec![
            6.223499, 6.207499, 6.2073326, 6.2073326, 6.2073326, 6.2073326, 6.2073326, 6.2073326,
            6.2073326, 6.2073326, 6.2073326, 6.2073326, 6.2073326, 6.2073326, 6.2073326, 6.2073326,
            6.2073326, 6.2073326, 6.2073326, 6.2073326, 6.2073326, 6.2073326, 6.1522994, 6.1522994,
            6.1522994, 6.1522994, 6.1522994, 6.1522994, 6.1522994, 6.1522994, 6.1522994, 6.1522994,
            6.1522994, 6.1580467, 6.1580467, 6.1580467,
        ];
        let expected_direction = vec![
            -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0,
            -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        ];

        let (direction, supertrend) = supertrend(&hl2, &close, &atr, factor);
        let result_direction: Vec<f32> = direction.into();
        let result_supertrend: Vec<f32> = supertrend.into();

        assert_eq!(high.len(), low.len());
        assert_eq!(high.len(), close.len());
        assert_eq!(result_direction, expected_direction);
        assert_eq!(result_supertrend, expected_supertrend);
    }
}
