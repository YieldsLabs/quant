use core::series::Series;

pub fn bullish(open: &[f64], high: &[f64], close: &[f64]) -> Vec<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let close = Series::from(close);

    (close.eq(&close.shift(1))
        & high.eq(&close.shift(1))
        & open.lt(&close.shift(1))
        & close.shift(1).lt(&open.shift(1))
        & close.gt(&open))
    .into()
}

pub fn bearish(open: &[f64], low: &[f64], close: &[f64]) -> Vec<bool> {
    let open = Series::from(open);
    let low = Series::from(low);
    let close = Series::from(close);

    (close.eq(&close.shift(1))
        & low.eq(&close.shift(1))
        & open.gt(&close.shift(1))
        & close.shift(1).gt(&open.shift(1))
        & close.lt(&open))
    .into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_on_neck_bullish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 5.0];
        let high = vec![3.5, 2.5, 3.5, 2.5, 4.5];
        let close = vec![4.5, 4.0, 5.0, 4.5, 5.5];
        let expected = vec![false, false, false, false, false];

        let result = bullish(&open, &high, &close);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_on_neck_bearish() {
        let open = vec![4.0, 5.0, 4.0, 5.0, 4.0];
        let low = vec![4.5, 5.5, 4.5, 5.5, 4.5];
        let close = vec![3.5, 4.0, 3.5, 4.0, 3.5];
        let expected = vec![false, false, false, false, false];

        let result = bearish(&open, &low, &close);

        assert_eq!(result, expected);
    }
}
