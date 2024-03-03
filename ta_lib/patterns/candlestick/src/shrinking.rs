use core::prelude::*;

pub fn bullish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    let prev_high = high.shift(1);
    let back_2_high = high.shift(2);
    let back_3_high = high.shift(3);

    let back_2_low = low.shift(2);

    close.sgt(open)
        & close.sgt(&prev_high)
        & close.sgt(&back_2_high)
        & close.sgt(&back_3_high)
        & prev_high.slt(&back_2_high)
        & back_2_high.slt(&back_3_high)
        & low.shift(1).seq(&back_2_low)
        & back_2_low.seq(&low.shift(3))
        & close.shift(4).slt(&open.shift(4))
}

pub fn bearish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    let prev_low = low.shift(1);
    let back_2_low = low.shift(2);
    let back_3_low = low.shift(3);

    let back_2_high = high.shift(2);

    close.slt(open)
        & close.slt(&prev_low)
        & close.slt(&back_2_low)
        & close.slt(&back_3_low)
        & prev_low.slt(&back_2_low)
        & back_2_low.slt(&back_3_low)
        & high.shift(1).seq(&back_2_high)
        & back_2_high.seq(&high.shift(3))
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
