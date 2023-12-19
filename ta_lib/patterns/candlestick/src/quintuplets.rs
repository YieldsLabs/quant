use core::{Comparator, Series};

pub fn bullish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    let body = (open - close).abs();

    close.sgt(open)
        & close.sgt(&close.shift(1))
        & body.slt(&body.shift(1))
        & close.shift(1).sgt(&open.shift(1))
        & close.shift(1).sgt(&close.shift(2))
        & body.shift(1).slt(&body.shift(2))
        & close.shift(2).sgt(&open.shift(2))
        & close.shift(2).sgt(&close.shift(3))
        & body.shift(2).slt(&body.shift(3))
        & close.shift(3).sgt(&open.shift(3))
        & close.shift(3).sgt(&close.shift(4))
        & body.shift(3).slt(&body.shift(4))
        & close.shift(4).sgt(&open.shift(4))
        & body.shift(4).slt(&body.shift(5))
}

pub fn bearish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    let body = (open - close).abs();

    close.slt(open)
        & close.slt(&close.shift(1))
        & body.slt(&body.shift(1))
        & close.shift(1).slt(&open.shift(1))
        & close.shift(1).slt(&close.shift(2))
        & body.shift(1).slt(&body.shift(2))
        & close.shift(2).slt(&open.shift(2))
        & close.shift(2).slt(&close.shift(3))
        & body.shift(2).slt(&body.shift(3))
        & close.shift(3).slt(&open.shift(3))
        & close.shift(3).slt(&close.shift(4))
        & body.shift(3).slt(&body.shift(4))
        & close.shift(4).slt(&open.shift(4))
        & body.shift(4).slt(&body.shift(5))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_quintuplets_bullish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 4.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_quintuplets_bearish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 4.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
