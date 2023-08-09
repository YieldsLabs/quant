use core::series::Series;

pub fn stoch(high: &[f32], low: &[f32], close: &[f32], period: usize) -> Series<f32> {
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    let hh = high.highest(period);
    let ll = low.lowest(period);

    let stoch = 100.0 * (close - &ll) / (hh - ll);

    stoch
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stoch() {
        let high = vec![3.0, 3.0, 3.0, 3.0, 3.0];
        let low = vec![1.0, 1.0, 1.0, 1.0, 1.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];
        let period = 3;

        let expected = vec![Some(50.0), Some(75.0), Some(50.0), Some(25.0), Some(50.0)];

        let result = stoch(&high, &low, &close, period);

        assert_eq!(result, expected);
    }
}
