use core::prelude::*;

pub fn bullish(open: &Price, high: &Price, low: &Price, close: &Price) -> Rule {
    let prev_high = high.shift(1);
    let back_2_high = high.shift(2);

    let back_2_low = low.shift(2);

    back_2_high.sgt(&high.shift(3))
        & back_2_low.slt(&low.shift(3))
        & close.shift(2).slt(&open.shift(2))
        & prev_high.slt(&back_2_high)
        & low.shift(1).sgt(&back_2_low)
        & high.sgt(&prev_high)
}

pub fn bearish(open: &Price, high: &Price, low: &Price, close: &Price) -> Rule {
    let prev_low = low.shift(1);
    let back_2_low = low.shift(2);

    let back_2_high = high.shift(2);

    back_2_high.sgt(&high.shift(3))
        & back_2_low.slt(&low.shift(3))
        & close.shift(2).slt(&open.shift(2))
        & high.shift(1).slt(&back_2_high)
        & prev_low.sgt(&back_2_low)
        & low.slt(&prev_low)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_three_one_two_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let low = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let close = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_three_one_two_bearish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let close = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
