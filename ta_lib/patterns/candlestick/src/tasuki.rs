use core::series::Series;

pub fn bullish(open: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    close.lt(&open)
        & close.shift(1).gt(&open.shift(1))
        & close.shift(2).gt(&open.shift(2))
        & close.lt(&open.shift(1))
        & close.gt(&close.shift(2))
        & open.shift(1).gt(&close.shift(2))
}

pub fn bearish(open: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    close.gt(&open)
        & close.shift(1).lt(&open.shift(1))
        & close.shift(2).lt(&open.shift(2))
        & close.gt(&open.shift(1))
        & close.lt(&close.shift(2))
        & open.shift(1).lt(&close.shift(2))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tasuki_bullish() {
        let open = vec![4.0, 4.0, 4.0, 4.0, 4.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_tasuki_bearish() {
        let open = vec![4.0, 4.0, 4.0, 4.0, 4.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
