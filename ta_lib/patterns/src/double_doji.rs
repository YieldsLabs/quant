use core::series::Series;

pub fn bullish(open: &[f64], close: &[f64]) -> Vec<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    (close.shift(1).eq_series(&open.shift(1))
        & close.shift(2).eq_series(&open.shift(2))
        & close.shift(3).lt_series(&open.shift(3)))
    .into()
}

pub fn bearish(open: &[f64], close: &[f64]) -> Vec<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    (close.shift(1).eq_series(&open.shift(1))
        & close.shift(2).eq_series(&open.shift(2))
        & close.shift(3).gt_series(&open.shift(3)))
    .into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_double_doji_bullish() {
        let open = vec![4.0, 4.0, 4.0, 4.0, 5.0];
        let close = vec![5.0, 3.0, 4.0, 4.0, 6.0];
        let expected = vec![false, false, false, false, true];

        let result = bullish(&open, &close);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_double_doji_bearish() {
        let open = vec![4.0, 4.0, 4.0, 6.0, 5.0];
        let close = vec![5.0, 5.0, 4.0, 6.0, 4.0];
        let expected = vec![false, false, false, false, true];

        let result = bearish(&open, &close);

        assert_eq!(result, expected);
    }
}
