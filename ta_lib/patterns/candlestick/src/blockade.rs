use core::prelude::*;

pub fn bullish(open: &Price, high: &Price, low: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);
    let close_4_back = close.shift(4);

    let prev_low = low.shift(1);
    let low_2_back = low.shift(2);
    let low_3_back = low.shift(3);
    let low_4_back = low.shift(4);

    let high_4_back = high.shift(4);

    prev_close.sgt(&open.shift(1))
        & close_4_back.slt(&open.shift(4))
        & prev_low.sgte(&low_4_back)
        & prev_low.slte(&close_4_back)
        & prev_close.sgt(&high_4_back)
        & low_2_back.sgte(&low_4_back)
        & low_2_back.slte(&close_4_back)
        & low_3_back.sgte(&low_4_back)
        & low_3_back.slte(&close_4_back)
        & high.shift(2).slt(&high_4_back)
        & high.shift(3).slt(&high_4_back)
}

pub fn bearish(open: &Price, high: &Price, low: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);
    let close_4_back = close.shift(4);

    let prev_high = high.shift(1);
    let high_2_back = high.shift(2);
    let high_3_back = high.shift(3);
    let high_4_back = high.shift(4);

    let low_4_back = low.shift(4);

    prev_close.slt(&open.shift(1))
        & close_4_back.sgt(&open.shift(4))
        & prev_high.slte(&high_4_back)
        & prev_high.sgte(&close_4_back)
        & prev_close.slt(&low_4_back)
        & high_2_back.slte(&high_4_back)
        & high_2_back.sgte(&close_4_back)
        & high_3_back.slte(&high_4_back)
        & high_3_back.sgte(&close_4_back)
        & low.shift(2).sgt(&low_4_back)
        & low.shift(3).sgt(&low_4_back)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_blockade_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let low = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let close = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_blockade_bearish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let close = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
