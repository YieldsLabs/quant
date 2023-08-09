use core::series::Series;

pub fn bullish(open: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    close.gt(&open)
        & close.shift(1).lt(&open.shift(1))
        & open.lt(&close.shift(1))
        & close.lt(&open.shift(1))
        & close.gte(&((close.shift(1) + open.shift(1)) / 2.0))
}

pub fn bearish(open: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    close.lt(&open)
        & close.shift(1).gt(&open.shift(1))
        & open.gt(&close.shift(1))
        & close.gt(&open.shift(1))
        & close.lte(&((close.shift(1) + open.shift(1)) / 2.0))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_piercing_bullish() {
        let open = vec![4.0, 4.0, 4.0, 4.0, 4.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_piercing_bearish() {
        let open = vec![4.0, 4.0, 4.0, 4.0, 4.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
