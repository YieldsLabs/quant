use core::series::Series;

pub fn bullish(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Vec<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    (close.shift(1).gt_series(&open.shift(1))
        & high.shift(1).eq_series(&close.shift(1))
        & low.shift(1).eq_series(&open.shift(1)))
    .into()
}

pub fn bearish(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Vec<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    (close.shift(1).lt_series(&open.shift(1))
        & high.shift(1).eq_series(&open.shift(1))
        & low.shift(1).eq_series(&close.shift(1)))
    .into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_marubozu_bullish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let low = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let close = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let expected = vec![false, true, true, true, true];

        let result = bullish(&open, &high, &low, &close);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_marubozu_bearish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let low = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let close = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let expected = vec![false, true, true, true, true];

        let result = bearish(&open, &high, &low, &close);

        assert_eq!(result, expected);
    }
}
