use core::series::Series;

pub fn bullish(open: &[f32], high: &[f32], low: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    close.gt(&high.shift(3))
        & close.gt(&close.shift(4))
        & low.shift(1).lt(&open)
        & close.shift(1).lt(&close)
        & high.shift(1).lte(&high.shift(3))
        & low.shift(2).lt(&open)
        & close.shift(2).lt(&close)
        & high.shift(2).lte(&high.shift(3))
        & high.shift(3).lt(&high.shift(4))
        & low.shift(3).gt(&low.shift(4))
        & close.shift(4).gt(&open.shift(4))
}

pub fn bearish(open: &[f32], high: &[f32], low: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    close.lt(&low.shift(3))
        & close.lt(&close.shift(4))
        & high.shift(1).gt(&open)
        & close.shift(1).gt(&close)
        & low.shift(1).gte(&low.shift(3))
        & high.shift(2).gt(&open)
        & close.shift(2).gt(&close)
        & low.shift(2).gte(&low.shift(3))
        & low.shift(3).gt(&low.shift(4))
        & high.shift(3).lt(&high.shift(4))
        & close.shift(4).lt(&open.shift(4))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hikkake_bullish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let low = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let close = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_hikkake_bearish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let low = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let close = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
