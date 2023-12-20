use core::prelude::*;

pub fn bullish(open: &Series<f32>, low: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    close.shift(1).sgt(&open.shift(1))
        & close.shift(2).slt(&open.shift(2))
        & close.shift(3).slt(&open.shift(3))
        & low.shift(1).seq(&low.shift(2))
        & low.shift(2).seq(&low.shift(3))
}

pub fn bearish(open: &Series<f32>, high: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    close.shift(1).slt(&open.shift(1))
        & close.shift(2).sgt(&open.shift(2))
        & close.shift(3).sgt(&open.shift(3))
        & high.shift(1).seq(&high.shift(2))
        & high.shift(2).seq(&high.shift(3))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_barrier_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let low = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let close = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_barrier_bearish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let close = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &close).into();

        assert_eq!(result, expected);
    }
}
