use core::Series;

pub fn bullish(open: &Series<f32>, high: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    close.eq(&close.shift(1))
        & high.eq(&close.shift(1))
        & open.lt(&close.shift(1))
        & close.shift(1).lt(&open.shift(1))
        & close.gt(open)
}

pub fn bearish(open: &Series<f32>, low: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    close.eq(&close.shift(1))
        & low.eq(&close.shift(1))
        & open.gt(&close.shift(1))
        & close.shift(1).gt(&open.shift(1))
        & close.lt(open)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_on_neck_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 5.0]);
        let high = Series::from([3.5, 2.5, 3.5, 2.5, 4.5]);
        let close = Series::from([4.5, 4.0, 5.0, 4.5, 5.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_on_neck_bearish() {
        let open = Series::from([4.0, 5.0, 4.0, 5.0, 4.0]);
        let low = Series::from([4.5, 5.5, 4.5, 5.5, 4.5]);
        let close = Series::from([3.5, 4.0, 3.5, 4.0, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &low, &close).into();

        assert_eq!(result, expected);
    }
}
