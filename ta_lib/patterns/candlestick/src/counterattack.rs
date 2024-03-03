use core::prelude::*;

pub fn bullish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    let prev_close = close.shift(1);

    open.slt(&prev_close)
        & close.sgt(open)
        & prev_close.slt(&open.shift(1))
        & close.seq(&prev_close)
}

pub fn bearish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    let prev_close = close.shift(1);

    open.sgt(&prev_close)
        & close.slt(open)
        & prev_close.sgt(&open.shift(1))
        & close.seq(&prev_close)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_counterattack_bullish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 4.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_counterattack_bearish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 4.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
