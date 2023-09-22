use core::Series;

pub fn bullish(open: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    close.shift(1).eq(&open.shift(1))
        & close.shift(2).eq(&open.shift(2))
        & close.shift(3).lt(&open.shift(3))
}

pub fn bearish(open: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    close.shift(1).eq(&open.shift(1))
        & close.shift(2).eq(&open.shift(2))
        & close.shift(3).gt(&open.shift(3))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_double_doji_bullish() {
        let open = vec![4.0, 4.0, 4.0, 4.0, 5.0];
        let close = vec![5.0, 3.0, 4.0, 4.0, 6.0];
        let expected = vec![false, false, false, false, true];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_double_doji_bearish() {
        let open = vec![4.0, 4.0, 4.0, 6.0, 5.0];
        let close = vec![5.0, 5.0, 4.0, 6.0, 4.0];
        let expected = vec![false, false, false, false, true];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
