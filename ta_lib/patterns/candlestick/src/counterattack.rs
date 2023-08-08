use core::series::Series;

pub fn bullish(open: &[f64], close: &[f64]) -> Series<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    open.lt(&close.shift(1))
        & close.gt(&open)
        & close.shift(1).lt(&open.shift(1))
        & close.eq(&close.shift(1))
}

pub fn bearish(open: &[f64], close: &[f64]) -> Series<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    open.gt(&close.shift(1))
        & close.lt(&open)
        & close.shift(1).gt(&open.shift(1))
        & close.eq(&close.shift(1))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_counterattack_bullish() {
        let open = vec![4.0, 4.0, 4.0, 4.0, 4.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_counterattack_bearish() {
        let open = vec![4.0, 4.0, 4.0, 4.0, 4.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
