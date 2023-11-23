use core::{iff, Series};

pub fn ast(close: &Series<f32>, atr: &Series<f32>, factor: f32) -> (Series<f32>, Series<f32>) {
    let atr_multi = atr * factor;

    let len = close.len();
    let mut trend = Series::zero(len);

    let up = close - &atr_multi;
    let dn = close + &atr_multi;
    let prev_close = close.shift(1);

    for _ in 0..len {
        let prev_trend = trend.shift(1);

        trend = iff!(close.gt(&prev_trend), up, dn);
        trend = iff!(
            close.lt(&prev_trend) & prev_close.lt(&prev_trend),
            prev_trend.min(&dn),
            trend
        );
        trend = iff!(
            close.gt(&prev_trend) & prev_close.gt(&prev_trend),
            prev_trend.max(&up),
            trend
        );
    }

    let mut direction = Series::zero(len);
    let trend_up = Series::fill(1.0, len);
    let trend_dn = Series::fill(-1.0, len);

    for _ in 0..len {
        let prev_direction = direction.shift(1);
        let prev_trend = trend.shift(1);
        direction = iff!(
            prev_close.gt(&prev_trend) & close.lt(&prev_trend),
            trend_dn,
            prev_direction
        );
        direction = iff!(
            prev_close.lt(&prev_trend) & close.gt(&prev_trend),
            trend_up,
            direction
        )
    }

    (direction, trend)
}

#[cfg(test)]
mod tests {
    use super::*;
    use volatility::atr;

    #[test]
    fn test_ast() {
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
        let expected_trend = vec![
            2.0885003, 2.0885003, 2.0840998, 2.0856998, 2.0856998, 2.0856998, 2.0856998, 2.0856998,
            2.0856998, 2.0856998, 2.0856998, 2.0856998, 2.0856998, 2.0905805, 2.0905805, 2.0905805,
            2.0905805, 2.0905805, 2.0985756,
        ];
        let expected_direction = vec![
            0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, -1.0,
        ];

        let (direction, trend) = ast(&close, &atr, factor);
        let result_direction: Vec<f32> = direction.into();
        let result_trend: Vec<f32> = trend.into();

        assert_eq!(high.len(), low.len());
        assert_eq!(high.len(), close.len());
        assert_eq!(result_trend, expected_trend);
        assert_eq!(result_direction, expected_direction);
    }
}
