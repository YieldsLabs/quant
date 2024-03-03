use core::prelude::*;

pub fn bullish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    let prev_close = close.shift(1);
    let prev_open = open.shift(1);

    close.slt(&prev_open)
        & open.sge(&prev_close)
        & high.slt(&high.shift(1))
        & low.sgt(&low.shift(1))
        & close.sgt(open)
        & prev_close.slt(&prev_open)
        & close.shift(2).slt(&open.shift(2))
}

pub fn bearish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    let prev_close = close.shift(1);
    let prev_open = open.shift(1);

    close.sgt(&prev_open)
        & open.sle(&prev_close)
        & high.slt(&high.shift(1))
        & low.sgt(&low.shift(1))
        & close.slt(open)
        & prev_close.sgt(&prev_open)
        & close.shift(2).sgt(&open.shift(2))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_harami_flexible_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let low = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let close = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_harami_flexible_bearish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let close = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
