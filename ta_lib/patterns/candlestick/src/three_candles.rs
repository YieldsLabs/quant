use core::prelude::*;

pub fn bullish(open: &Price, close: &Price) -> Rule {
    let body = (open - close).abs();

    let prev_close = close.shift(1);
    let back_2_close = close.shift(2);

    let prev_back = body.shift(1);
    let back_2_body = body.shift(2);

    close.sgt(&prev_close)
        & prev_close.sgt(&back_2_close)
        & back_2_close.sgt(&close.shift(3))
        & body.sgte(&body.highest(5))
        & prev_back.sgte(&prev_back.highest(5))
        & back_2_body.sgte(&back_2_body.highest(5))
}

pub fn bearish(open: &Price, close: &Price) -> Rule {
    let body = (open - close).abs();

    let prev_close = close.shift(1);
    let back_2_close = close.shift(2);

    let prev_back = body.shift(1);
    let back_2_body = body.shift(2);

    close.slt(&prev_close)
        & prev_close.slt(&back_2_close)
        & back_2_close.slt(&close.shift(3))
        & body.sgte(&body.highest(5))
        & prev_back.sgte(&prev_back.highest(5))
        & back_2_body.sgte(&back_2_body.highest(5))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_three_candles_bullish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 4.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_three_candles_bearish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 4.0]);
        let close = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
