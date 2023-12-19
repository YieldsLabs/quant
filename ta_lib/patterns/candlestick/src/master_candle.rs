use core::{Comparator, Series};

pub fn bullish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    close.sgt(&high.shift(6))
        & close.sgt(open)
        & high.shift(1).slt(&high.shift(6))
        & low.shift(1).sgt(&low.shift(6))
        & high.shift(2).slt(&high.shift(6))
        & low.shift(2).sgt(&low.shift(6))
        & high.shift(3).slt(&high.shift(6))
        & low.shift(3).sgt(&low.shift(6))
        & high.shift(4).slt(&high.shift(6))
        & low.shift(4).sgt(&low.shift(6))
        & high.shift(5).slt(&high.shift(6))
        & low.shift(5).sgt(&low.shift(6))
}

pub fn bearish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    close.slt(&low.shift(6))
        & close.slt(open)
        & high.shift(1).slt(&high.shift(6))
        & low.shift(1).sgt(&low.shift(6))
        & high.shift(2).slt(&high.shift(6))
        & low.shift(2).sgt(&low.shift(6))
        & high.shift(3).slt(&high.shift(6))
        & low.shift(3).sgt(&low.shift(6))
        & high.shift(4).slt(&high.shift(6))
        & low.shift(4).sgt(&low.shift(6))
        & high.shift(5).slt(&high.shift(6))
        & low.shift(5).sgt(&low.shift(6))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_master_candle_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0, 6.0]);
        let high = Series::from([4.5, 3.5, 4.5, 3.5, 4.5, 5.0]);
        let low = Series::from([4.0, 3.0, 4.0, 3.0, 4.0, 3.6]);
        let close = Series::from([4.5, 3.5, 4.5, 3.5, 4.5, 4.5]);
        let expected = vec![false, false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_master_candle_bearish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0, 6.0]);
        let high = Series::from([4.0, 3.0, 4.0, 3.0, 4.0, 5.0]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 3.5, 3.4]);
        let close = Series::from([3.5, 2.5, 3.5, 2.5, 3.5, 5.6]);
        let expected = vec![false, false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
