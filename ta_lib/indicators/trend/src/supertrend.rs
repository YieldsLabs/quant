use core::{iff, Series};

pub fn supertrend(
    hl2: &Series<f32>,
    close: &Series<f32>,
    atr: &Series<f32>,
    factor: f32,
) -> Series<f32> {
    let len = close.len();

    let basic_upper_band = hl2 + (atr * factor);
    let basic_lower_band = hl2 - (atr * factor);

    let prev_final_upper_band = basic_upper_band.shift(1);
    let prev_final_lower_band = basic_lower_band.shift(1);
    let prev_close = close.shift(1);

    let final_upper_band = iff!(
        basic_upper_band.lt(&prev_final_upper_band) | prev_close.gt(&prev_final_upper_band),
        basic_upper_band,
        prev_final_upper_band
    );

    let final_lower_band = iff!(
        basic_lower_band.gt(&prev_final_lower_band) | prev_close.lt(&prev_final_lower_band),
        basic_lower_band,
        prev_final_lower_band
    );

    let super_trend = iff!(
        prev_close.gte(&final_lower_band),
        final_lower_band,
        Series::empty(len)
    );

    iff!(
        prev_close.lte(&final_upper_band),
        final_upper_band,
        super_trend
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
            0.0, 19.871502, 19.88732, 19.88732, 19.861986, 19.85842, 19.830359, 19.817736,
            19.757202, 19.70696, 19.67325, 19.634144, 19.59141, 19.59141, 19.609882, 19.597612,
            19.597612, 19.586113, 19.586113, 19.5795, 19.54907,
        ];

        let result: Vec<f32> = supertrend(&hl2, &close, &atr, factor).into();

        assert_eq!(result, expected);
    }
}
