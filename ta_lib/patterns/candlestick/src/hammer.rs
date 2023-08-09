use core::series::Series;

pub fn bullish(open: &[f32], high: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let close = Series::from(close);

    let body = (&close - &open).abs();

    close.shift(1).gt(&open.shift(1))
        & close.shift(2).gt(&open.shift(2))
        & close.shift(2).eq(&high.shift(2))
        & close.shift(3).lt(&open.shift(3))
        & body.shift(2).lt(&body.shift(1))
        & body.shift(2).lt(&body.shift(3))
}

pub fn bearish(open: &[f32], low: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let low = Series::from(low);
    let close = Series::from(close);

    let body = (&close - &open).abs();

    close.shift(1).lt(&open.shift(1))
        & close.shift(2).lt(&open.shift(2))
        & close.shift(2).eq(&low.shift(2))
        & close.shift(3).gt(&open.shift(3))
        & body.shift(2).lt(&body.shift(1))
        & body.shift(2).lt(&body.shift(3))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hammer_bullish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 5.0];
        let high = vec![3.5, 2.5, 3.5, 2.5, 4.5];
        let close = vec![4.5, 4.0, 5.0, 4.5, 5.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_hammer_bearish() {
        let open = vec![4.0, 5.0, 4.0, 5.0, 4.0];
        let low = vec![4.5, 5.5, 4.5, 5.5, 4.5];
        let close = vec![3.5, 4.0, 3.5, 4.0, 3.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &low, &close).into();

        assert_eq!(result, expected);
    }
}
