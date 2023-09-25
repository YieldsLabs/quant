use core::Series;

pub fn bullish(open: &Series<f32>, low: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    close.shift(2).gt(&open.shift(2))
        & close.shift(1).gt(&open.shift(1))
        & open.shift(1).lt(&close.shift(2))
        & open.shift(1).eq(&low.shift(1))
        & close.shift(1).gt(&close.shift(2))
}

pub fn bearish(open: &Series<f32>, high: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    close.shift(2).lt(&open.shift(2))
        & close.shift(1).lt(&open.shift(1))
        & open.shift(1).gt(&close.shift(2))
        & open.shift(1).eq(&high.shift(1))
        & close.shift(1).lt(&close.shift(2))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bottle_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 5.0]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 4.5]);
        let close = Series::from([4.5, 4.0, 5.0, 4.5, 5.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_bottle_bearish() {
        let open = Series::from([4.0, 5.0, 4.0, 5.0, 4.0]);
        let high = Series::from([4.5, 5.5, 4.5, 5.5, 4.5]);
        let close = Series::from([3.5, 4.0, 3.5, 4.0, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &close).into();

        assert_eq!(result, expected);
    }
}
