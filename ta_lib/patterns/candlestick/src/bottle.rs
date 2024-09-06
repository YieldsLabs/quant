use core::prelude::*;

pub fn bullish(open: &Price, low: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);
    let back_2_close = close.shift(2);

    let prev_open = open.shift(1);

    back_2_close.sgt(&open.shift(2))
        & prev_close.sgt(&prev_open)
        & prev_open.slt(&back_2_close)
        & prev_open.seq(&low.shift(1))
        & prev_close.sgt(&back_2_close)
}

pub fn bearish(open: &Price, high: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);
    let back_2_close = close.shift(2);

    let prev_open = open.shift(1);

    back_2_close.slt(&open.shift(2))
        & prev_close.slt(&prev_open)
        & prev_open.sgt(&back_2_close)
        & prev_open.seq(&high.shift(1))
        & prev_close.slt(&back_2_close)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bottle_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 5.0]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 4.5]);
        let close = Series::from([4.5, 4.0, 5.0, 4.5, 5.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_bottle_bearish() {
        let open = Series::from([4.0, 5.0, 4.0, 5.0, 4.0]);
        let high = Series::from([4.5, 5.5, 4.5, 5.5, 4.5]);
        let close = Series::from([3.5, 4.0, 3.5, 4.0, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &close).into();

        assert_eq!(result, expected);
    }
}
