use core::series::Series;

pub fn bullish(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Vec<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    (close.gt(&open)
        & close.gt(&high.shift(1))
        & close.gt(&high.shift(2))
        & close.gt(&high.shift(3))
        & high.shift(1).lt(&high.shift(2))
        & high.shift(2).lt(&high.shift(3))
        & low.shift(1).eq(&low.shift(2))
        & low.shift(2).eq(&low.shift(3))
        & close.shift(4).lt(&open.shift(4)))
    .into()
}

pub fn bearish(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Vec<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    (close.lt(&open)
        & close.lt(&low.shift(1))
        & close.lt(&low.shift(2))
        & close.lt(&low.shift(3))
        & low.shift(1).lt(&low.shift(2))
        & low.shift(2).lt(&low.shift(3))
        & high.shift(1).eq(&high.shift(2))
        & high.shift(2).eq(&high.shift(3))
        & close.shift(4).gt(&open.shift(4)))
    .into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_shrinking_bullish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let low = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let close = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let expected = vec![false, false, false, false, false];

        let result = bullish(&open, &high, &low, &close);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_shrinking_bearish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let low = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let close = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let expected = vec![false, false, false, false, false];

        let result = bearish(&open, &high, &low, &close);

        assert_eq!(result, expected);
    }
}
