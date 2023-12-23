use core::prelude::*;

pub fn dch(
    high: &Series<f32>,
    low: &Series<f32>,
    period: usize,
) -> (Series<f32>, Series<f32>, Series<f32>) {
    let upper_band = high.highest(period);
    let lower_band = low.lowest(period);

    let middle_band = (&upper_band + &lower_band) / 2.;

    (upper_band, middle_band, lower_band)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dch() {
        let high = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let low = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let period = 3;
        let expected_upper = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected_lower = vec![1.0, 1.0, 1.0, 2.0, 3.0];

        let expected_middle = vec![1.0, 1.5, 2.0, 3.0, 4.0];

        let (upper, middle, lower) = dch(&high, &low, period);

        let result_upper: Vec<f32> = upper.into();
        let result_lower: Vec<f32> = lower.into();
        let result_middle: Vec<f32> = middle.into();

        assert_eq!(result_upper, expected_upper);
        assert_eq!(result_lower, expected_lower);
        assert_eq!(result_middle, expected_middle);
    }
}
