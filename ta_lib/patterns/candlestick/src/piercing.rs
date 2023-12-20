use core::prelude::*;

pub fn bullish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    close.sgt(open)
        & close.shift(1).slt(&open.shift(1))
        & open.slt(&close.shift(1))
        & close.slt(&open.shift(1))
        & close.sge(&((close.shift(1) + open.shift(1)) / 2.0))
}

pub fn bearish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    close.slt(open)
        & close.shift(1).sgt(&open.shift(1))
        & open.sgt(&close.shift(1))
        & close.sgt(&open.shift(1))
        & close.sle(&((close.shift(1) + open.shift(1)) / 2.0))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_piercing_bullish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 4.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_piercing_bearish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 4.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
