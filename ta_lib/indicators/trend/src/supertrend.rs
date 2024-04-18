use core::prelude::*;

pub fn supertrend(
    hl2: &Series<f32>,
    close: &Series<f32>,
    atr: &Series<f32>,
    factor: f32,
) -> (Series<f32>, Series<f32>) {
    let atr_mul = atr * factor;

    let mut up = hl2 - &atr_mul;
    let mut dn = hl2 + &atr_mul;

    let len = hl2.len();

    let mut prev_up = up.shift(1);
    let mut prev_dn = dn.shift(1);
    
    prev_up = iff!(prev_up.na(), up, prev_up);
    prev_dn = iff!(prev_dn.na(), dn, prev_dn);

    for _ in 0..len {
        let prev_close = close.shift(1);
        up = iff!(prev_close.sgt(&prev_up), up.max(&prev_up), up);
        dn = iff!(prev_close.slt(&prev_dn), dn.min(&prev_dn), dn);
    }

    let mut direction = Series::one(len);
    let trend_bull = Series::one(len);
    let trend_bear = trend_bull.negate();

    for _ in 0..len {
        let prev_direction = direction.shift(1);

        direction = iff!(prev_direction.na(), direction, prev_direction);

        direction = iff!(
            direction.seq(&ONE) & close.slt(&prev_up),
            trend_bear,
            direction
        );
        direction = iff!(
            direction.seq(&MINUS_ONE) & close.sgt(&prev_dn),
            trend_bull,
            direction
        );
    }

    let mut supertrend = iff!(direction.seq(&MINUS_ONE), dn, Series::zero(len));
    supertrend = iff!(direction.seq(&ONE), up, supertrend);

    (direction, supertrend)
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::prelude::*;
    use volatility::atr;

    #[test]
    fn test_supertrend() {
        let high = Series::from([6.5600, 6.6049, 6.5942, 6.5541, 6.5300, 6.5700, 6.5630]);
        let low = Series::from([6.5418, 6.5394, 6.5301, 6.4782, 6.4882, 6.5131, 6.5126]);
        let close = Series::from([6.5541, 6.5942, 6.5348, 6.4950, 6.5298, 6.5616, 6.5223]);
        let hl2 = median_price(&high, &low);
        let atr_period = 2;
        let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);

        let factor = 3.0;
        let expected_supertrend = vec![
            6.4963, 6.4963, 6.446601, 6.403225, 6.3497434, 6.376522, 6.3796854,
        ];
        let expected_direction = vec![
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        ];

        let (direction, supertrend) = supertrend(&hl2, &close, &atr, factor);
        let result_direction: Vec<f32> = direction.into();
        let result_supertrend: Vec<f32> = supertrend.into();

        assert_eq!(high.len(), low.len());
        assert_eq!(high.len(), close.len());
        assert_eq!(result_supertrend, expected_supertrend);
        assert_eq!(result_direction, expected_direction);
    }
}
