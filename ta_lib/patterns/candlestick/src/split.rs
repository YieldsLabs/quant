use core::series::Series;

pub fn bullish(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    close.shift(1).lt(&open.shift(1))
        & open.shift(1).lt(&high.shift(1))
        & close.shift(1).eq(&low.shift(1))
        & close.gt(&open)
        & close.eq(&high)
        & open.gt(&low)
        & close.gt(&open.shift(1))
}

pub fn bearish(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    close.shift(1).gt(&open.shift(1))
        & open.shift(1).gt(&low.shift(1))
        & close.shift(1).eq(&high.shift(1))
        & close.lt(&open)
        & close.eq(&low)
        & open.lt(&high)
        & close.lt(&open.shift(1))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_split_bullish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let low = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let close = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_split_bearish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let low = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let close = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
