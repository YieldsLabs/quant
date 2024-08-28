use core::prelude::*;

pub fn bullish(low: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);
    let back_2_close = close.shift(2);
    let prev_low = low.shift(1);
    let back_2_low = low.shift(2);

    low.sgt(&prev_low)
        & prev_low.sgt(&back_2_low)
        & back_2_low.slt(&low.shift(3))
        & close.sgt(&prev_close)
        & prev_close.sgt(&back_2_close)
        & back_2_close.sgt(&close.shift(3))
}

pub fn bearish(high: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);
    let back_2_close = close.shift(2);
    let prev_high = high.shift(1);
    let back_2_high = high.shift(2);

    high.slt(&prev_high)
        & prev_high.slt(&back_2_high)
        & back_2_high.sgt(&high.shift(3))
        & close.slt(&prev_close)
        & prev_close.slt(&back_2_close)
        & back_2_close.slt(&close.shift(3))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_r_bullish() {
        let low = Series::from([0.4818, 0.4815, 0.4812, 0.4836, 0.4850]);
        let close = Series::from([0.4822, 0.4818, 0.4837, 0.4856, 0.4888]);
        let expected = vec![false, false, false, false, true];

        let result: Vec<bool> = bullish(&low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_r_bearish() {
        let high = Series::from([0.4802, 0.4807, 0.4808, 0.4796, 0.4791]);
        let close = Series::from([0.4801, 0.4799, 0.4794, 0.4785, 0.4783]);
        let expected = vec![false, false, false, false, true];

        let result: Vec<bool> = bearish(&high, &close).into();

        assert_eq!(result, expected);
    }
}
