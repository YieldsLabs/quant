use core::prelude::*;

pub fn bullish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    let prev_close = close.shift(1);
    let prev_open = open.shift(1);

    close.sgt(open)
        & prev_close.slt(&prev_open)
        & open.slt(&prev_close)
        & close.slt(&prev_open)
        & close.sgte(&(0.5 * (prev_close + prev_open)))
}

pub fn bearish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    let prev_close = close.shift(1);
    let prev_open = open.shift(1);

    close.slt(open)
        & prev_close.sgt(&prev_open)
        & open.sgt(&prev_close)
        & close.sgt(&prev_open)
        & close.slte(&(0.5 * (prev_close + prev_open)))
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
