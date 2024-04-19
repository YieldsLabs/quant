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

    let basic_up = source - &atr_mul;
    let mut up = Series::zero(len);

    for _ in 0..len {
        let prev_up = nz!(up.shift(1), basic_up);
        up = iff!(
            basic_up.sgt(&prev_up) | prev_close.slt(&prev_up),
            basic_up,
            prev_up
        );
    }

    let basic_dn = source + &atr_mul;
    let mut dn = Series::zero(len);

    for _ in 0..len {
        let prev_dn = nz!(dn.shift(1), basic_dn);
        dn = iff!(
            basic_dn.slt(&prev_dn) | prev_close.sgt(&prev_dn),
            basic_dn,
            prev_dn
        );
    }

    let mut direction = Series::one(len);
    let trend_bull = Series::one(len);
    let trend_bear = trend_bull.negate();

    for _ in 0..len {
        direction = nz!(direction.shift(1), direction);

        let cond_bull = direction.seq(&MINUS_ONE) & close.sgt(&dn.shift(1));
        let cond_bear = direction.seq(&ONE) & close.slt(&up.shift(1));

        direction = iff!(
            cond_bull,
            trend_bull,
            iff!(cond_bear, trend_bear, direction)
        );
    }

    let supertrend = iff!(
        direction.seq(&MINUS_ONE),
        dn,
        iff!(direction.seq(&ONE), up, Series::zero(len))
    );

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
            6.5425, 6.5527, 6.5600, 6.6049, 6.5942, 6.5541, 6.5300, 6.5700, 6.5630, 6.5362, 6.5497,
            6.5480, 6.5325, 6.5065, 6.4866, 6.5536, 6.5142, 6.5294, 6.5543, 6.5563,
        ]);
        let low = Series::from([
            6.5156, 6.5195, 6.5418, 6.5394, 6.5301, 6.4782, 6.4882, 6.5131, 6.5126, 6.5184, 6.5206,
            6.5229, 6.4982, 6.4560, 6.4614, 6.4798, 6.4903, 6.5066, 6.5231, 6.5222,
        ]);
        let close = Series::from([
            6.5232, 6.5474, 6.5541, 6.5942, 6.5348, 6.4950, 6.5298, 6.5616, 6.5223, 6.5300, 6.5452,
            6.5254, 6.5038, 6.4614, 6.4854, 6.4966, 6.5117, 6.5270, 6.5527, 6.5316,
        ]);
        let hl2 = median_price(&high, &low);
        let atr_period = 3;
        let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);

        let factor = 3.0;
        let expected_supertrend = vec![
            6.4483504, 6.4491, 6.4747, 6.4747, 6.4747, 6.4747, 6.4747, 6.4747, 6.4747, 6.4747,
            6.4747, 6.4747, 6.4747, 6.5986347, 6.5774565, 6.5774565, 6.5774565, 6.5774565,
            6.5774565, 6.5774565,
        ];
        let expected_direction = vec![
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0,
            -1.0, -1.0, -1.0, -1.0,
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
