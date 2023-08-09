use core::series::Series;

pub fn bullish(open: &[f32], high: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let close = Series::from(close);

    close.eq(&close.shift(1))
        & high.eq(&close.shift(1))
        & open.lt(&close.shift(1))
        & close.shift(1).lt(&open.shift(1))
        & close.gt(&open)
}

pub fn bearish(open: &[f32], low: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let low = Series::from(low);
    let close = Series::from(close);

    close.eq(&close.shift(1))
        & low.eq(&close.shift(1))
        & open.gt(&close.shift(1))
        & close.shift(1).gt(&open.shift(1))
        & close.lt(&open)
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

        let result: Vec<bool> = bullish(&open, &high, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_on_neck_bearish() {
        let open = vec![4.0, 5.0, 4.0, 5.0, 4.0];
        let low = vec![4.5, 5.5, 4.5, 5.5, 4.5];
        let close = vec![3.5, 4.0, 3.5, 4.0, 3.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &low, &close).into();

        assert_eq!(result, expected);
    }
}
