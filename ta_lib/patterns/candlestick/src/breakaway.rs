use core::prelude::*;

pub fn bullish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    let back_3_open = open.shift(3);
    let back_4_close = close.shift(4);

    close.sgt(&back_3_open)
        & close.sgt(open)
        & close.shift(1).slt(&open.shift(1))
        & close.shift(2).slt(&open.shift(2))
        & close.shift(3).slt(&back_3_open)
        & back_4_close.slt(&open.shift(4))
        & back_3_open.slt(&back_4_close)
}

pub fn bearish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    let back_3_open = open.shift(3);
    let back_4_close = close.shift(4);

    close.slt(&back_3_open)
        & close.slt(open)
        & close.shift(1).sgt(&open.shift(1))
        & close.shift(2).sgt(&open.shift(2))
        & close.shift(3).sgt(&back_3_open)
        & back_4_close.sgt(&open.shift(4))
        & back_3_open.sgt(&back_4_close)
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
