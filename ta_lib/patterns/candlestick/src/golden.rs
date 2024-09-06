use core::prelude::*;

const GOLDEN_RATIO: Scalar = 2.618;

pub fn bullish(open: &Price, high: &Price, low: &Price, close: &Price) -> Rule {
    let back_2_low = low.shift(2);
    let golden_low = &back_2_low + GOLDEN_RATIO * (high.shift(2) - &back_2_low);

    low.slte(&open.shift(1)) & close.shift(1).sgt(&golden_low) & close.shift(2).sgt(&open.shift(2))
}

pub fn bearish(open: &Price, high: &Price, low: &Price, close: &Price) -> Rule {
    let back_2_high = high.shift(2);
    let golden_high = &back_2_high - GOLDEN_RATIO * (&back_2_high - low.shift(2));

    high.sgte(&open.shift(1))
        & close.shift(1).slt(&golden_high)
        & close.shift(2).slt(&open.shift(2))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_golden_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 5.0]);
        let high = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 4.5]);
        let close = Series::from([4.5, 4.0, 5.0, 4.5, 5.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_golden_bearish() {
        let open = Series::from([4.0, 5.0, 4.0, 5.0, 4.0]);
        let high = Series::from([4.5, 5.5, 4.5, 5.5, 4.5]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 4.5]);
        let close = Series::from([3.5, 4.0, 3.5, 4.0, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
