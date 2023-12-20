use core::prelude::*;

pub fn bullish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    close.sgt(&open.shift(3))
        & close.sgt(open)
        & close.shift(1).slt(&open.shift(1))
        & close.shift(2).slt(&open.shift(2))
        & close.shift(3).slt(&open.shift(3))
        & close.shift(4).slt(&open.shift(4))
        & open.shift(3).slt(&close.shift(4))
}

pub fn bearish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    close.slt(&open.shift(3))
        & close.slt(open)
        & close.shift(1).sgt(&open.shift(1))
        & close.shift(2).sgt(&open.shift(2))
        & close.shift(3).sgt(&open.shift(3))
        & close.shift(4).sgt(&open.shift(4))
        & open.shift(3).sgt(&close.shift(4))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_breakaway_bullish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 5.0]);
        let close = Series::from([5.0, 4.0, 3.0, 4.0, 6.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_breakaway_bearish() {
        let open = Series::from([4.0, 4.0, 4.0, 6.0, 5.0]);
        let close = Series::from([5.0, 4.0, 5.0, 6.0, 4.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
