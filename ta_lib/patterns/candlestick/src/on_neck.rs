use core::prelude::*;

pub fn bullish(open: &Price, high: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);

    close.seq(&prev_close)
        & high.seq(&prev_close)
        & open.slt(&prev_close)
        & prev_close.slt(&open.shift(1))
        & close.sgt(open)
}

pub fn bearish(open: &Price, low: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);

    close.seq(&prev_close)
        & low.seq(&prev_close)
        & open.sgt(&prev_close)
        & prev_close.sgt(&open.shift(1))
        & close.slt(open)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_on_neck_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 5.0]);
        let high = Series::from([3.5, 2.5, 3.5, 2.5, 4.5]);
        let close = Series::from([4.5, 4.0, 5.0, 4.5, 5.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_on_neck_bearish() {
        let open = Series::from([4.0, 5.0, 4.0, 5.0, 4.0]);
        let low = Series::from([4.5, 5.5, 4.5, 5.5, 4.5]);
        let close = Series::from([3.5, 4.0, 3.5, 4.0, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &low, &close).into();

        assert_eq!(result, expected);
    }
}
