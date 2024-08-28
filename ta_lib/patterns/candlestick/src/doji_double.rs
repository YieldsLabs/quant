use core::prelude::*;

pub fn bullish(open: &Price, close: &Price) -> Rule {
    close.shift(1).seq(&open.shift(1))
        & close.shift(2).seq(&open.shift(2))
        & close.shift(3).slt(&open.shift(3))
}

pub fn bearish(open: &Price, close: &Price) -> Rule {
    close.shift(1).seq(&open.shift(1))
        & close.shift(2).seq(&open.shift(2))
        & close.shift(3).sgt(&open.shift(3))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_double_doji_bullish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 5.0]);
        let close = Series::from([5.0, 3.0, 4.0, 4.0, 6.0]);
        let expected = vec![false, false, false, false, true];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_double_doji_bearish() {
        let open = Series::from([4.0, 4.0, 4.0, 6.0, 5.0]);
        let close = Series::from([5.0, 5.0, 4.0, 6.0, 4.0]);
        let expected = vec![false, false, false, false, true];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
