use core::prelude::*;

pub fn bullish(open: &Series<f32>, high: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    close.sgt(open)
        & close.shift(1).sgt(&open.shift(1))
        & close.shift(2).sgt(&open.shift(2))
        & close.shift(3).slt(&open.shift(3))
        & close.shift(4).slt(&open.shift(4))
        & close.shift(5).slt(&open.shift(5))
        & close.sgt(&high.shift(5))
}

pub fn bearish(open: &Series<f32>, low: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    close.slt(open)
        & close.shift(1).slt(&open.shift(1))
        & close.shift(2).slt(&open.shift(2))
        & close.shift(3).sgt(&open.shift(3))
        & close.shift(4).sgt(&open.shift(4))
        & close.shift(5).sgt(&open.shift(5))
        & close.slt(&low.shift(5))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hexad_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 5.0]);
        let high = Series::from([3.5, 2.5, 3.5, 2.5, 4.5]);
        let close = Series::from([4.5, 4.0, 5.0, 4.5, 5.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_hexad_bearish() {
        let open = Series::from([4.0, 5.0, 4.0, 5.0, 4.0]);
        let low = Series::from([4.5, 5.5, 4.5, 5.5, 4.5]);
        let close = Series::from([3.5, 4.0, 3.5, 4.0, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &low, &close).into();

        assert_eq!(result, expected);
    }
}
