use core::Series;

pub fn stoch(
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
    period: usize,
) -> Series<f32> {
    let hh = high.highest(period);
    let ll = low.lowest(period);

    100.0 * (close - &ll) / (hh - ll)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stoch() {
        let high = Series::from([3.0, 3.0, 3.0, 3.0, 3.0]);
        let low = Series::from([1.0, 1.0, 1.0, 1.0, 1.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let period = 3;

        let expected = vec![Some(50.0), Some(75.0), Some(50.0), Some(25.0), Some(50.0)];

        let result = stoch(&high, &low, &close, period);

        assert_eq!(result, expected);
    }
}
