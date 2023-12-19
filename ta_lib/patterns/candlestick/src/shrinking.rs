use core::{Comparator, Series};

pub fn bullish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    close.sgt(open)
        & close.sgt(&high.shift(1))
        & close.sgt(&high.shift(2))
        & close.sgt(&high.shift(3))
        & high.shift(1).slt(&high.shift(2))
        & high.shift(2).slt(&high.shift(3))
        & low.shift(1).seq(&low.shift(2))
        & low.shift(2).seq(&low.shift(3))
        & close.shift(4).slt(&open.shift(4))
}

pub fn bearish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    close.slt(open)
        & close.slt(&low.shift(1))
        & close.slt(&low.shift(2))
        & close.slt(&low.shift(3))
        & low.shift(1).slt(&low.shift(2))
        & low.shift(2).slt(&low.shift(3))
        & high.shift(1).seq(&high.shift(2))
        & high.shift(2).seq(&high.shift(3))
        & close.shift(4).sgt(&open.shift(4))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_shrinking_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let low = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let close = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_shrinking_bearish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let close = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
