use core::series::Series;

pub fn bullish(open: &[f32], high: &[f32], low: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    close.shift(1).gt(&open.shift(1))
        & close.shift(4).lt(&open.shift(4))
        & low.shift(1).gte(&low.shift(4))
        & low.shift(1).lte(&close.shift(4))
        & close.shift(1).gt(&high.shift(4))
        & low.shift(2).gte(&low.shift(4))
        & low.shift(2).lte(&close.shift(4))
        & low.shift(3).gte(&low.shift(4))
        & low.shift(3).lte(&close.shift(4))
        & high.shift(2).lt(&high.shift(4))
        & high.shift(3).lt(&high.shift(4))
}

pub fn bearish(open: &[f32], high: &[f32], low: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    close.shift(1).lt(&open.shift(1))
        & close.shift(4).gt(&open.shift(4))
        & high.shift(1).lte(&high.shift(4))
        & high.shift(1).gte(&close.shift(4))
        & close.shift(1).lt(&low.shift(4))
        & high.shift(2).lte(&high.shift(4))
        & high.shift(2).gte(&close.shift(4))
        & high.shift(3).lte(&high.shift(4))
        & high.shift(3).gte(&close.shift(4))
        & low.shift(2).gt(&low.shift(4))
        & low.shift(3).gt(&low.shift(4))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_blockade_bullish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let low = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let close = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_blockade_bearish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let low = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let close = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
