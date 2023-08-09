use core::series::Series;

pub fn bullish(open: &[f32], high: &[f32], low: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    let body = (&close - &open).abs();

    close.gt(&open)
        & close.shift(1).lt(&open.shift(1))
        & high.gt(&high.shift(1))
        & low.lt(&low.shift(1))
        & body.gte(&(2.0 * body.shift(1)))
}

pub fn bearish(open: &[f32], high: &[f32], low: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    let body = (&close - &open).abs();

    close.lt(&open)
        & close.shift(1).gt(&open.shift(1))
        & high.gt(&high.shift(1))
        & low.lt(&low.shift(1))
        & body.gte(&(2.0 * body.shift(1)))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_engulfing_bullish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let low = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let close = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_engulfing_bearish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let low = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let close = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
