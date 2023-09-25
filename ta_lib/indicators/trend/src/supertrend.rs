use core::{iff, Series};

pub fn supertrend(
    hl2: &Series<f32>,
    close: &Series<f32>,
    atr: &Series<f32>,
    factor: f32,
) -> Series<f32> {
    let len = close.len();

    let mut upper_band = hl2 + (atr * factor);
    let mut lower_band = hl2 - (atr * factor);

    let prev_up = upper_band.shift(1);
    let prev_low = lower_band.shift(1);

    let prev_upper_band = iff!(prev_up.na(), prev_up, upper_band);
    let prev_lower_band = iff!(prev_low.na(), prev_low, lower_band);
    let prev_close = close.shift(1);

    let final_upper_band = iff!(
        prev_close.lt(&prev_upper_band),
        upper_band.min(&prev_upper_band),
        prev_upper_band
    );

    let final_lower_band = iff!(
        prev_close.gt(&prev_lower_band),
        lower_band.max(&prev_lower_band),
        prev_lower_band
    );

    iff!(
        prev_close.lte(&final_upper_band),
        final_upper_band,
        iff!(
            prev_close.gte(&final_lower_band),
            final_lower_band,
            Series::empty(len)
        )
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::median_price;
    use volatility::atr;

    #[test]
    fn test_supertrend() {
        let high = Series::from([
            19.579, 19.619, 19.589, 19.617, 19.594, 19.596, 19.580, 19.580, 19.534, 19.485, 19.445,
            19.418, 19.376, 19.401, 19.394, 19.382, 19.394, 19.382, 19.394, 19.382, 19.351,
        ]);
        let low = Series::from([
            19.462, 19.492, 19.502, 19.554, 19.506, 19.526, 19.516, 19.520, 19.446, 19.386, 19.383,
            19.333, 19.288, 19.316, 19.311, 19.312, 19.325, 19.307, 19.325, 19.307, 19.304,
        ]);
        let close = Series::from([
            19.538, 19.554, 19.577, 19.568, 19.587, 19.539, 19.549, 19.530, 19.450, 19.417, 19.398,
            19.376, 19.371, 19.374, 19.363, 19.348, 19.370, 19.325, 19.370, 19.325, 19.329,
        ]);
        let hl2 = median_price(&high, &low);
        let atr_period = 7;
        let atr = atr(&high, &low, &close, atr_period, Some("SMMA"));
        let factor = 3.0;
        let expected = vec![
            0.0, 19.609928, 19.62944, 19.684448, 19.672525, 19.696024, 19.691162, 19.698423,
            19.654936, 19.619303, 19.598116, 19.569742, 19.53621, 19.569963, 19.569326, 19.562849,
            19.574085, 19.560572, 19.574278, 19.560736, 19.532988,
        ];

        let result: Vec<f32> = supertrend(&hl2, &close, &atr, factor).into();

        assert_eq!(result, expected);
    }
}
