use core::{iff, Comparator, Series};

pub fn dmi(
    high: &Series<f32>,
    low: &Series<f32>,
    atr: &Series<f32>,
    adx_period: usize,
    di_period: usize,
) -> (Series<f32>, Series<f32>, Series<f32>) {
    let up = high.change(1);
    let down = low.change(1).neg();

    let zero = Series::zero(high.len());

    let dm_plus = iff!(up.sgt(&down) & up.sgt(&0.0), up, zero);
    let dm_minus = iff!(down.sgt(&up) & down.sgt(&0.0), down, zero);

    let di_plus = 100.0 * dm_plus.smma(di_period) / atr;
    let di_minus = 100.0 * dm_minus.smma(di_period) / atr;

    let sum = &di_plus + &di_minus;
    let one = Series::fill(1.0, high.len());

    let adx =
        100.0 * ((&di_plus - &di_minus).abs() / iff!(sum.seq(&0.0), one, sum)).smma(adx_period);

    (adx, di_plus, di_minus)
}

#[cfg(test)]
mod tests {
    use super::*;
    use volatility::atr;

    #[test]
    fn test_dmi() {
        let high = Series::from([
            6.8430, 6.8660, 6.8685, 6.8690, 6.865, 6.8595, 6.8565, 6.862, 6.859, 6.86, 6.8580,
            6.8605, 6.8620, 6.86, 6.859, 6.8670, 6.8640, 6.8575, 6.8485, 6.8450, 6.8365, 6.84,
            6.8385, 6.8365, 6.8345, 6.8395,
        ]);
        let low = Series::from([
            6.8380, 6.8430, 6.8595, 6.8640, 6.8435, 6.8445, 6.8510, 6.8560, 6.8520, 6.8530, 6.8550,
            6.8550, 6.8565, 6.8475, 6.8480, 6.8535, 6.8565, 6.8455, 6.8445, 6.8365, 6.8310, 6.8310,
            6.8345, 6.8325, 6.8275, 6.8285,
        ]);
        let close = Series::from([
            6.6430, 6.8595, 6.8680, 6.8650, 6.8445, 6.8560, 6.8565, 6.8590, 6.8530, 6.8575, 6.855,
            6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365, 6.8310, 6.8355,
            6.8360, 6.8345, 6.8285, 6.8395,
        ]);
        let adx_period = 3;
        let di_period = 3;
        let atr = atr(&high, &low, &close, adx_period, Some("SMMA"));

        let expected_adx = [
            0.0, 33.333336, 55.555557, 70.37037, 61.10112, 54.921627, 50.801956, 38.320854,
            32.417755, 24.420816, 19.089525, 23.014332, 31.298655, 38.86024, 43.9013, 41.01218,
            39.0861, 43.248535, 47.322624, 57.331203, 66.542816, 57.70211, 51.808304, 52.638172,
            60.376694, 41.247677,
        ];
        let expected_di_plus = [
            0.0, 9.871335, 10.852027, 10.814587, 8.438895, 6.86148, 6.221794, 17.530615, 14.233753,
            14.244971, 12.47987, 20.861288, 22.631794, 11.659865, 7.109966, 28.910229, 21.441114,
            13.234582, 11.108815, 7.347112, 5.529561, 18.132135, 14.484046, 11.126235, 6.9170723,
            25.08336,
        ];
        let expected_di_minus = [
            0.0, 0.0, 0.0, 0.0, 20.94579, 17.030563, 15.442828, 13.398855, 21.624754, 16.866737,
            14.776772, 11.021119, 7.9791555, 39.016933, 23.791792, 13.845649, 10.26855, 41.423733,
            38.785717, 57.523396, 68.031395, 42.329178, 33.812767, 37.56404, 50.37606, 26.629393,
        ];

        let (result_adx, result_di_plus, result_di_minus) =
            dmi(&high, &low, &atr, adx_period, di_period);

        let adx: Vec<f32> = result_adx.into();
        let di_plus: Vec<f32> = result_di_plus.into();
        let di_minus: Vec<f32> = result_di_minus.into();

        assert_eq!(adx, expected_adx);
        assert_eq!(di_plus, expected_di_plus);
        assert_eq!(di_minus, expected_di_minus);
    }
}
