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
    let hlc3 = Series::from(typical_price(&high, &low, &close));
    let atr = atr(&high, &low, &close, atr_period, None) * factor;

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
        let high = vec![2.0, 4.0, 6.0];
        let low = vec![1.0, 2.0, 3.0];
        let close = vec![1.5, 3.0, 4.5];
        let period = 3;
        let atr_period = 3;
        let factor = 2.0;
        let epsilon = 0.001;
        let expected_upper_band = vec![1.5, 3.9166667, 6.486111];
        let expected_middle_band = vec![1.5, 2.25, 3.375];
        let expected_lower_band = vec![1.5, 0.58333325, 0.26388884];

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
