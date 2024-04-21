use core::prelude::*;

pub fn supertrend(
    source: &Series<f32>,
    close: &Series<f32>,
    atr: &Series<f32>,
    factor: f32,
) -> (Series<f32>, Series<f32>) {
    let atr_mul = atr * factor;
    let prev_close = close.shift(1);
    let len = close.len();

    let mut up = source - &atr_mul;
    let mut dn = source + &atr_mul;
    let mut direction = Series::empty(len);
    let mut supertrend = Series::empty(len);

    let trend_bull = Series::one(len);
    let trend_bear = trend_bull.negate();
    direction = iff!(&atr.shift(1).na(), trend_bull, direction);

    for _ in 0..len {
        let prev_up = nz!(up.shift(1), up);
        up = iff!(up.sgt(&prev_up) | prev_close.slt(&prev_up), up, prev_up);

        let prev_dn = nz!(dn.shift(1), dn);
        dn = iff!(dn.slt(&prev_dn) | prev_close.sgt(&prev_dn), dn, prev_dn);

        let prev_supertrend = supertrend.shift(1);

        direction = iff!(
            &atr.shift(1).na(),
            trend_bull,
            iff!(
                prev_supertrend.seq(&prev_dn),
                iff!(close.sgt(&dn), trend_bear, trend_bull),
                iff!(close.slt(&up), trend_bull, trend_bear)
            )
        );

        supertrend = iff!(direction.seq(&MINUS_ONE), up, dn);
    }

    (direction, supertrend)
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::prelude::*;
    use volatility::atr;

    #[test]
    fn test_supertrend() {
        let high = Series::from([
            6.622, 6.650, 6.664, 6.687, 6.695, 6.647, 6.624, 6.607, 6.609, 6.614, 6.609, 6.590,
            6.580, 6.580, 6.586, 6.587, 6.586, 6.574, 6.584, 6.577, 6.578, 6.583, 6.575, 6.577,
            6.578, 6.567, 6.575, 6.588, 6.596, 6.600, 6.587, 6.573, 6.566, 6.586,
        ]);
        let low = Series::from([
            6.582, 6.614, 6.636, 6.637, 6.602, 6.606, 6.576, 6.579, 6.579, 6.587, 6.562, 6.566,
            6.559, 6.551, 6.567, 6.556, 6.560, 6.541, 6.543, 6.564, 6.560, 6.557, 6.557, 6.565,
            6.559, 6.552, 6.563, 6.567, 6.575, 6.570, 6.570, 6.541, 6.552, 6.555,
        ]);
        let close = Series::from([
            6.617, 6.645, 6.641, 6.679, 6.627, 6.624, 6.593, 6.607, 6.588, 6.608, 6.581, 6.579,
            6.569, 6.574, 6.574, 6.578, 6.568, 6.543, 6.577, 6.571, 6.563, 6.575, 6.565, 6.573,
            6.567, 6.563, 6.571, 6.578, 6.596, 6.574, 6.572, 6.556, 6.555, 6.579,
        ]);
        let hl2 = median_price(&high, &low);
        let atr_period = 3;
        let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);

        let factor = 3.0;
        let expected_supertrend = vec![
            6.7220016, 6.7220016, 6.7220016, 6.7220016, 6.7220016, 6.7220016, 6.7220016, 6.7220016,
            6.71035, 6.7050667, 6.7022114, 6.679808, 6.658372, 6.653748, 6.653748, 6.653748,
            6.653748, 6.644672, 6.644672, 6.644672, 6.639718, 6.639718, 6.632763, 6.627509,
            6.6251726, 6.6122813, 6.6122813, 6.6122813, 6.6122813, 6.6122813, 6.6122813, 6.6122813,
            6.6122813, 6.6122813,
        ];
        let expected_direction = vec![
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
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
