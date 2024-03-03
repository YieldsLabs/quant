use core::prelude::*;

pub fn bullish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    let prev_close = close.shift(1);
    let back_2_close = close.shift(2);

    let prev_open = open.shift(1);
    let back_2_open = open.shift(2);

    close.shift(3).slt(&open.shift(3))
        & high.shift(2).seq(&high.shift(1))
        & low.shift(2).seq(&low.shift(1))
        & prev_close
            .max(&prev_open)
            .seq(&back_2_close.max(&back_2_open))
        & prev_close
            .min(&prev_open)
            .seq(&back_2_close.min(&back_2_open))
}

pub fn bearish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    let prev_close = close.shift(1);
    let back_2_close = close.shift(2);

    let prev_open = open.shift(1);
    let back_2_open = open.shift(2);

    close.shift(3).sgt(&open.shift(3))
        & high.shift(2).seq(&high.shift(1))
        & low.shift(2).seq(&low.shift(1))
        & prev_close
            .max(&prev_open)
            .seq(&back_2_close.max(&back_2_open))
        & prev_close
            .min(&prev_open)
            .seq(&back_2_close.min(&back_2_open))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_doppelganger_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let low = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let close = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_doppelganger_bearish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let close = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
