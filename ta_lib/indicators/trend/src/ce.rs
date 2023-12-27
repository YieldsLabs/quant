use core::prelude::*;

pub fn ce(
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
    atr: &Series<f32>,
    period: usize,
    factor: f32,
) -> (Series<f32>, Series<f32>) {
    let atr_multi = atr * factor;

    let short_stop = low.lowest(period) + &atr_multi;
    let long_stop = high.highest(period) - &atr_multi;

    let len = close.len();
    let mut short = Series::empty(len);
    let mut long = Series::empty(len);

    for _ in 0..len {
        let prev_short = short.shift(1);
        short = iff!(
            close.sgt(&prev_short),
            short_stop,
            short_stop.min(&prev_short)
        );
        short = iff!(prev_short.na(), short_stop, short);

        let prev_long = long.shift(1);
        long = iff!(close.slt(&prev_long), long_stop, long.max(&prev_long));
        long = iff!(prev_long.na(), long_stop, long);
    }

    let mut direction = Series::empty(len);
    let trend_up = Series::one(len);
    let trend_dn = trend_up.negate();
    let trend_middle = Series::zero(len);
    let prev_close = close.shift(1);

    let long_switch = iff!(
        close.sge(&short.shift(1)) & prev_close.slt(&short.shift(1)),
        trend_up,
        trend_middle
    );
    let short_switch = iff!(
        close.sle(&long.shift(1)) & prev_close.sgt(&long.shift(1)),
        trend_up,
        trend_middle
    );

    for _ in 0..len {
        let prev_direction = direction.shift(1);
        let cond_one = prev_direction.sle(&trend_middle) & long_switch.clone().into();
        let cond_two = prev_direction.sge(&trend_middle) & short_switch.clone().into();

        direction = iff!(
            prev_direction.na(),
            trend_middle,
            iff!(cond_one, trend_up, iff!(cond_two, trend_dn, prev_direction))
        );
    }

    let trend = iff!(direction.sgt(&trend_middle), long, short);

    (direction, trend)
}

#[cfg(test)]
mod tests {
    use super::*;
    use volatility::atr;

    #[test]
    fn test_ce() {
        let high = Series::from([
            2.0859, 2.0881, 2.0889, 2.0896, 2.0896, 2.0907, 2.0919, 2.1004, 2.0936, 2.0939, 2.0972,
            2.0974, 2.0997, 2.0982, 2.0982, 2.0974, 2.0942, 2.0924, 2.0924,
        ]);
        let low = Series::from([
            2.0846, 2.0846, 2.0881, 2.0886, 2.0865, 2.0875, 2.0886, 2.0909, 2.0899, 2.0912, 2.0934,
            2.0947, 2.0946, 2.0973, 2.0942, 2.0920, 2.0908, 2.0917, 2.0869,
        ]);
        let close = Series::from([
            2.0846, 2.0881, 2.0889, 2.0896, 2.0875, 2.0904, 2.0909, 2.0936, 2.0912, 2.0939, 2.0949,
            2.0952, 2.0973, 2.0982, 2.0974, 2.0942, 2.0917, 2.0924, 2.0869,
        ]);
        let atr_period = 2;
        let atr = atr(&high, &low, &close, atr_period, Some("SMMA"));

        let factor = 3.0;
        let period = 3;
        let expected_trend = vec![
            2.0885003, 2.0885003, 2.0840998, 2.0856998, 2.0856998, 2.0856998, 2.0856998, 2.0856998,
            2.0856998, 2.0888877, 2.0888877, 2.0888877, 2.0888877, 2.0920804, 2.0920804, 2.0920804,
            2.100978, 2.0976512, 2.0976512,
        ];
        let expected_direction = vec![
            0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0,
            -1.0, -1.0,
        ];

        let (direction, trend) = ce(&high, &low, &close, &atr, period, factor);
        let result_direction: Vec<f32> = direction.into();
        let result_trend: Vec<f32> = trend.into();

        assert_eq!(high.len(), low.len());
        assert_eq!(high.len(), close.len());
        assert_eq!(result_trend, expected_trend);
        assert_eq!(result_direction, expected_direction);
    }
}
