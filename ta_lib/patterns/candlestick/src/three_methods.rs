use core::prelude::*;

pub fn bullish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    let prev_low = low.shift(1);
    let back_4_low = low.shift(4);

    let back_4_close = close.shift(4);

    close.sgt(open)
        & close.sgt(&high.shift(4))
        & low.slt(&prev_low)
        & close.shift(1).slt(&back_4_close)
        & prev_low.sgt(&back_4_low)
        & close.shift(2).slt(&back_4_close)
        & low.shift(2).sgt(&back_4_low)
        & close.shift(3).slt(&back_4_close)
        & low.shift(3).sgt(&back_4_low)
        & back_4_close.sgt(&open.shift(4))
}

pub fn bearish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    let prev_high = high.shift(1);
    let back_4_high = high.shift(4);

    let back_4_close = close.shift(4);

    close.slt(open)
        & close.slt(&low.shift(4))
        & high.sgt(&prev_high)
        & close.shift(1).sgt(&back_4_close)
        & prev_high.slt(&back_4_high)
        & close.shift(2).sgt(&back_4_close)
        & high.shift(2).slt(&back_4_high)
        & close.shift(3).sgt(&back_4_close)
        & high.shift(3).slt(&back_4_high)
        & back_4_close.slt(&open.shift(4))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_three_methods_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let low = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let close = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_three_methods_bearish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let close = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
