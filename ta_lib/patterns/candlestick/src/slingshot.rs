use core::prelude::*;

pub fn bullish(open: &Price, high: &Price, low: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);
    let close_3_back = close.shift(3);
    let close_4_back = close.shift(4);

    prev_close.sgt(&open.shift(1))
        & prev_close.sgt(&high.shift(2))
        & prev_close.sgt(&high.shift(3))
        & close.shift(2).slt(&open.shift(2))
        & close_3_back.sgt(&open.shift(3))
        & close_4_back.sgt(&open.shift(4))
        & close_3_back.sgt(&close_4_back)
        & low.shift(1).sgt(&close_4_back)
}

pub fn bearish(open: &Price, high: &Price, low: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);
    let back_3_close = close.shift(3);
    let back_4_close = close.shift(4);

    prev_close.slt(&open.shift(1))
        & prev_close.slt(&low.shift(2))
        & prev_close.slt(&low.shift(3))
        & close.shift(2).sgt(&open.shift(2))
        & back_3_close.slt(&open.shift(3))
        & back_4_close.slt(&open.shift(4))
        & back_3_close.slt(&back_4_close)
        & high.shift(1).slt(&back_4_close)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sligshot_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let low = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let close = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_sligshot_bearish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let close = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
