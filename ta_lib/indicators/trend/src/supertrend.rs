use core::{iff, Series};

pub fn supertrend(
    hl2: &Series<f32>,
    close: &Series<f32>,
    atr: &Series<f32>,
    factor: f32,
) -> Series<f32> {
    let basic_upper_band = hl2 + (atr * factor);
    let basic_lower_band = hl2 - (atr * factor);

    let prev_upper_band = basic_upper_band.shift(1);
    let prev_lower_band = basic_lower_band.shift(1);

    let prev_final_upper_band = iff!(prev_upper_band.na(), basic_upper_band, prev_upper_band);
    let prev_final_lower_band = iff!(prev_lower_band.na(), basic_lower_band, prev_lower_band);
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

    let mut super_trend = iff!(
        final_lower_band.eq(&prev_final_lower_band) & close.lt(&final_lower_band),
        final_upper_band,
        final_upper_band
    );

    super_trend = iff!(
        final_lower_band.eq(&prev_final_lower_band) & close.gte(&final_lower_band),
        final_lower_band,
        super_trend
    );

    super_trend = iff!(
        final_lower_band.eq(&prev_final_upper_band) & close.gt(&final_upper_band),
        final_lower_band,
        super_trend
    );

    iff!(
        final_lower_band.eq(&prev_final_upper_band) & close.lte(&final_upper_band),
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
            6.86, 6.8580, 6.8605, 6.8620, 6.86, 6.8590, 6.8670, 6.8640, 6.8575, 6.8485, 6.8450,
            6.8365, 6.84, 6.8385, 6.8365,
        ]);
        let low = Series::from([
            6.8530, 6.8550, 6.8550, 6.8565, 6.8475, 6.8480, 6.8535, 6.8565, 6.8455, 6.8445, 6.8365,
            6.8310, 6.8310, 6.8345, 6.8325,
        ]);
        let close = Series::from([
            6.8575, 6.8550, 6.6580, 6.86, 6.8480, 6.8575, 6.8640, 6.8565, 6.8455, 6.8450, 6.8365,
            6.8310, 6.8355, 6.8360, 6.8345,
        ]);
        let hl2 = median_price(&high, &low);
        let atr_period = 3;
        let atr = atr(&high, &low, &close, atr_period, Some("SMMA"));
        let factor = 3.0;
        let expected = vec![
            6.8355002, 6.8734994, 6.8734994, 6.874583, 7.009732, 6.968488, 6.950409, 6.9278555,
            6.9085703, 6.8885465, 6.8044534, 6.804219, 6.863604, 6.859769, 6.854013,
        ];

        let result: Vec<f32> = supertrend(&hl2, &close, &atr, factor).into();

        assert_eq!(result, expected);
    }
}
