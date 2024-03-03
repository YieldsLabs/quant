use core::prelude::*;

pub fn bullish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    let body = (open - close).abs();

    let prev_close = close.shift(1);
    let back_2_close = close.shift(2);
    let back_3_close = close.shift(3);
    let back_4_close = close.shift(4);

    let prev_body = body.shift(1);
    let back_2_body = body.shift(2);
    let back_3_body = body.shift(3);
    let back_4_body = body.shift(4);

    close.sgt(open)
        & close.sgt(&prev_close)
        & body.slt(&prev_body)
        & prev_close.sgt(&open.shift(1))
        & prev_close.sgt(&back_2_close)
        & prev_body.slt(&back_2_body)
        & back_2_close.sgt(&open.shift(2))
        & back_2_close.sgt(&back_3_close)
        & back_2_body.slt(&back_3_body)
        & back_3_close.sgt(&open.shift(3))
        & back_3_close.sgt(&back_4_close)
        & back_3_body.slt(&back_4_body)
        & back_4_close.sgt(&open.shift(4))
        & back_4_body.slt(&body.shift(5))
}

pub fn bearish(open: &Series<f32>, close: &Series<f32>) -> Series<bool> {
    let body = (open - close).abs();

    let prev_close = close.shift(1);
    let back_2_close = close.shift(2);
    let back_3_close = close.shift(3);
    let back_4_close = close.shift(4);

    let prev_body = body.shift(1);
    let back_2_body = body.shift(2);
    let back_3_body = body.shift(3);
    let back_4_body = body.shift(4);

    close.slt(open)
        & close.slt(&prev_close)
        & body.slt(&prev_body)
        & prev_close.slt(&open.shift(1))
        & prev_close.slt(&back_2_close)
        & prev_body.slt(&back_2_body)
        & back_2_close.slt(&open.shift(2))
        & back_2_close.slt(&back_3_close)
        & back_2_body.slt(&back_3_body)
        & back_3_close.slt(&open.shift(3))
        & back_3_close.slt(&back_4_close)
        & back_3_body.slt(&back_4_body)
        & back_4_close.slt(&open.shift(4))
        & back_4_body.slt(&body.shift(5))
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
