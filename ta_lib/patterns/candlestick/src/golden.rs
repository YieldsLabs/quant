use core::series::Series;

pub fn bullish(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    let golden_low = low.shift(2) + 2.618 * (high.shift(2) - low.shift(2));

    low.lte(&open.shift(1)) & close.shift(1).gt(&golden_low) & close.shift(2).gt(&open.shift(2))
}

pub fn bearish(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    let golden_high = high.shift(2) - 2.618 * (high.shift(2) - low.shift(2));

    high.gte(&open.shift(1)) & close.shift(1).lt(&golden_high) & close.shift(2).lt(&open.shift(2))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_golden_bullish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 5.0];
        let high = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let low = vec![3.5, 2.5, 3.5, 2.5, 4.5];
        let close = vec![4.5, 4.0, 5.0, 4.5, 5.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_golden_bearish() {
        let open = vec![4.0, 5.0, 4.0, 5.0, 4.0];
        let high = vec![4.5, 5.5, 4.5, 5.5, 4.5];
        let low = vec![3.5, 2.5, 3.5, 2.5, 4.5];
        let close = vec![3.5, 4.0, 3.5, 4.0, 3.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
