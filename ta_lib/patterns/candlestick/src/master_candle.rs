use core::series::Series;

pub fn bullish(open: &[f32], high: &[f32], low: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    close.gt(&high.shift(6))
        & close.gt(&open)
        & high.shift(1).lt(&high.shift(6))
        & low.shift(1).gt(&low.shift(6))
        & high.shift(2).lt(&high.shift(6))
        & low.shift(2).gt(&low.shift(6))
        & high.shift(3).lt(&high.shift(6))
        & low.shift(3).gt(&low.shift(6))
        & high.shift(4).lt(&high.shift(6))
        & low.shift(4).gt(&low.shift(6))
        & high.shift(5).lt(&high.shift(6))
        & low.shift(5).gt(&low.shift(6))
}

pub fn bearish(open: &[f32], high: &[f32], low: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    close.lt(&low.shift(6))
        & close.lt(&open)
        & high.shift(1).lt(&high.shift(6))
        & low.shift(1).gt(&low.shift(6))
        & high.shift(2).lt(&high.shift(6))
        & low.shift(2).gt(&low.shift(6))
        & high.shift(3).lt(&high.shift(6))
        & low.shift(3).gt(&low.shift(6))
        & high.shift(4).lt(&high.shift(6))
        & low.shift(4).gt(&low.shift(6))
        & high.shift(5).lt(&high.shift(6))
        & low.shift(5).gt(&low.shift(6))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_master_candle_bullish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0, 6.0];
        let high = vec![4.5, 3.5, 4.5, 3.5, 4.5, 5.0];
        let low = vec![4.0, 3.0, 4.0, 3.0, 4.0, 3.6];
        let close = vec![4.5, 3.5, 4.5, 3.5, 4.5, 4.5];
        let expected = vec![false, false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_master_candle_bearish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0, 6.0];
        let high = vec![4.0, 3.0, 4.0, 3.0, 4.0, 5.0];
        let low = vec![3.5, 2.5, 3.5, 2.5, 3.5, 3.4];
        let close = vec![3.5, 2.5, 3.5, 2.5, 3.5, 5.6];
        let expected = vec![false, false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
