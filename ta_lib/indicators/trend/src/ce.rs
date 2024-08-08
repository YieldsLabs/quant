use core::prelude::*;

pub fn ce(
    close: &Series<f32>,
    atr: &Series<f32>,
    period: usize,
    factor: f32,
) -> (Series<f32>, Series<f32>) {
    let len = close.len();
    let atr_mul = atr * factor;

    let mut up = close.highest(period) - &atr_mul;
    let mut dn = close.lowest(period) + &atr_mul;

    let prev_close = close.shift(1);
    let mut direction = Series::one(len);

    let trend_bull = Series::one(len);
    let trend_bear = trend_bull.negate();

    for _ in 0..len {
        let prev_up = nz!(up.shift(1), up);
        up = iff!(prev_close.sgt(&prev_up), up.max(&prev_up), up);

        let prev_dn = nz!(dn.shift(1), dn);
        dn = iff!(prev_close.slt(&prev_dn), dn.min(&prev_dn), dn);

        direction = nz!(direction.shift(1), direction);
        direction = iff!(
            direction.seq(&MINUS_ONE) & close.sgt(&prev_dn),
            trend_bull,
            direction
        );
        direction = iff!(
            direction.seq(&ONE) & close.slt(&prev_up),
            trend_bear,
            direction
        );
    }

    let trend = iff!(direction.seq(&ONE), up, dn);

    (direction, trend)
}

#[cfg(test)]
mod tests {
    use super::*;
    use volatility::atr;

    #[test]
    fn test_ce_dn_up() {
        let high = Series::from([
            4.8217, 4.8285, 4.8225, 4.8146, 4.8019, 4.8115, 4.8160, 4.8142, 4.8179, 4.8506, 4.8819,
            4.8833, 4.8466, 4.8448, 4.8586,
        ]);
        let low = Series::from([
            4.7982, 4.8073, 4.8003, 4.7904, 4.7774, 4.7706, 4.7923, 4.7884, 4.7968, 4.8152, 4.8396,
            4.8393, 4.8275, 4.8300, 4.8397,
        ]);
        let close = Series::from([
            4.8122, 4.8112, 4.8122, 4.7973, 4.7800, 4.8039, 4.8047, 4.8115, 4.8152, 4.8414, 4.8814,
            4.8423, 4.8439, 4.8429, 4.8535,
        ]);
        let period = 3;
        let atr = atr(&high, &low, &close, Smooth::SMMA, period);

        let factor = 2.0;
        let expected_trend = vec![
            4.7652, 4.7667336, 4.767089, 4.767089, 4.767089, 4.767089, 4.767089, 4.767089, 4.767089, 4.784503, 4.815269, 4.815269, 4.81972, 4.81972, 4.81972,
        ];
        let expected_direction = vec![
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        ];

        let (direction, trend) = ce(&close, &atr, period, factor);
        let result_direction: Vec<f32> = direction.into();
        let result_trend: Vec<f32> = trend.into();

        assert_eq!(high.len(), low.len());
        assert_eq!(high.len(), close.len());
        assert_eq!(result_trend, expected_trend);
        assert_eq!(result_direction, expected_direction);
    }

    #[test]
    fn test_ce_up_dn() {
        let high = Series::from([
            4.8565, 4.8791, 4.9177, 4.9199, 4.9614, 4.9570, 4.9486, 4.9010, 4.9085, 4.8713, 4.8591,
            4.8660,
        ]);
        let low = Series::from([
            4.8113, 4.8447, 4.8696, 4.8858, 4.9128, 4.8955, 4.9005, 4.8551, 4.8447, 4.8325, 4.8333,
            4.8244,
        ]);
        let close = Series::from([
            4.8558, 4.8706, 4.9108, 4.9128, 4.9565, 4.9013, 4.9005, 4.8868, 4.8527, 4.8553, 4.8532,
            4.8305,
        ]);
        let period = 3;
        let atr = atr(&high, &low, &close, Smooth::SMMA, period);

        let factor = 2.0;
        let expected_trend = vec![
            4.7653995, 4.7874, 4.8232665, 4.831711, 4.8700404, 4.8700404, 4.8700404, 4.8700404, 4.959112, 4.949508, 4.9344387, 4.912726
        ];
        let expected_direction = vec![
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0,
        ];

        let (direction, trend) = ce(&close, &atr, period, factor);
        let result_direction: Vec<f32> = direction.into();
        let result_trend: Vec<f32> = trend.into();

        assert_eq!(high.len(), low.len());
        assert_eq!(high.len(), close.len());
        assert_eq!(result_trend, expected_trend);
        assert_eq!(result_direction, expected_direction);
    }
}
