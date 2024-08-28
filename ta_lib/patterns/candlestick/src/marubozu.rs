use core::prelude::*;

pub fn bullish(open: &Price, high: &Price, low: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);
    let prev_open = open.shift(1);

    prev_close.sgt(&prev_open) & high.shift(1).seq(&prev_close) & low.shift(1).seq(&prev_open)
}

pub fn bearish(open: &Price, high: &Price, low: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);
    let prev_open = open.shift(1);

    prev_close.slt(&prev_open) & high.shift(1).seq(&prev_open) & low.shift(1).seq(&prev_close)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_marubozu_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let low = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let close = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let expected = vec![false, true, true, true, true];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_marubozu_bearish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let close = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let expected = vec![false, true, true, true, true];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
