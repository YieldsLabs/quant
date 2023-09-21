use crate::atr;
use core::series::Series;
use price::typical_price;

pub fn kch(
    high: &[f32],
    low: &[f32],
    close: &[f32],
    period: usize,
    atr_period: usize,
    factor: f32,
) -> (Series<f32>, Series<f32>, Series<f32>) {
    let hlc3 = Series::from(typical_price(high, low, close));
    let atr = atr(high, low, close, atr_period, None) * factor;

    let middle_band = hlc3.ema(period);

    let upper_band = &middle_band + &atr;
    let lower_band = &middle_band - &atr;

    (upper_band, middle_band, lower_band)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kch() {
        let high = vec![
            19.129, 19.116, 19.154, 19.195, 19.217, 19.285, 19.341, 19.394, 19.450,
        ];
        let low = vec![
            19.090, 19.086, 19.074, 19.145, 19.141, 19.155, 19.219, 19.306, 19.355,
        ];
        let close = vec![
            19.102, 19.100, 19.146, 19.181, 19.155, 19.248, 19.309, 19.355, 19.439,
        ];
        let period = 3;
        let atr_period = 3;
        let factor = 2.0;
        let epsilon = 0.001;
        let expected_upper_band = [
            19.107, 19.123833, 19.180916, 19.221735, 19.259995, 19.348415, 19.426208, 19.478382,
            19.540155,
        ];
        let expected_middle_band = [
            19.107, 19.103834, 19.11425, 19.143959, 19.157478, 19.193405, 19.241535, 19.2966,
            19.355633,
        ];
        let expected_lower_band = [
            19.107, 19.083836, 19.047585, 19.066183, 19.054962, 19.038395, 19.056862, 19.114819,
            19.17111,
        ];

        let (upper_band, middle_band, lower_band) =
            kch(&high, &low, &close, period, atr_period, factor);

        let result_upper_band: Vec<f32> = upper_band.into();
        let result_middle_band: Vec<f32> = middle_band.into();
        let result_lower_band: Vec<f32> = lower_band.into();

        for i in 0..high.len() {
            let a = result_upper_band[i];
            let b = expected_upper_band[i];
            assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);

            let a = result_middle_band[i];
            let b = expected_middle_band[i];
            assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);

            let a = result_lower_band[i];
            let b = expected_lower_band[i];
            assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);
        }
    }
}
