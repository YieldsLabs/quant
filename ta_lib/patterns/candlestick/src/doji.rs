use core::prelude::*;

pub fn bullish(open: &Price, close: &Price) -> Rule {
    close.sgt(open) & close.shift(1).seq(&open.shift(1)) & close.shift(2).slt(&open.shift(2))
}

pub fn bearish(open: &Price, close: &Price) -> Rule {
    close.slt(open) & close.shift(1).seq(&open.shift(1)) & close.shift(2).sgt(&open.shift(2))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_doji_bullish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 5.0]);
        let close = Series::from([5.0, 4.0, 3.0, 4.0, 6.0]);
        let expected = vec![false, false, false, false, true];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_doji_bearish() {
        let open = Series::from([4.0, 4.0, 4.0, 6.0, 5.0]);
        let close = Series::from([5.0, 4.0, 5.0, 6.0, 4.0]);
        let expected = vec![false, false, false, false, true];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
