use core::prelude::*;

pub fn bullish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    let prev_open = open.shift(1);

    let back_2_close = close.shift(2);

    close.slt(open)
        & close.shift(1).sgt(&prev_open)
        & back_2_close.sgt(&open.shift(2))
        & close.slt(&prev_open)
        & close.sgt(&back_2_close)
        & prev_open.sgt(&back_2_close)
}

pub fn bearish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    let prev_open = open.shift(1);

    let back_2_close = close.shift(2);

    close.sgt(open)
        & close.shift(1).slt(&prev_open)
        & back_2_close.slt(&open.shift(2))
        & close.sgt(&prev_open)
        & close.slt(&back_2_close)
        & prev_open.slt(&back_2_close)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tasuki_bullish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 4.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_tasuki_bearish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 4.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
