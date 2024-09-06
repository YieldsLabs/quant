use core::prelude::*;

pub fn bullish(open: &Price, high: &Price, close: &Price) -> Rule {
    let body = (close - open).abs();

    let back_2_body = body.shift(2);

    close.shift(1).sgt(&open.shift(1))
        & close.shift(2).sgt(&open.shift(2))
        & close.shift(2).seq(&high.shift(2))
        & close.shift(3).slt(&open.shift(3))
        & back_2_body.slt(&body.shift(1))
        & back_2_body.slt(&body.shift(3))
}

pub fn bearish(open: &Price, low: &Price, close: &Price) -> Rule {
    let body = (close - open).abs();

    let back_2_body = body.shift(2);

    close.shift(1).slt(&open.shift(1))
        & close.shift(2).slt(&open.shift(2))
        & close.shift(2).seq(&low.shift(2))
        & close.shift(3).sgt(&open.shift(3))
        & back_2_body.slt(&body.shift(1))
        & back_2_body.slt(&body.shift(3))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hammer_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 5.0]);
        let high = Series::from([3.5, 2.5, 3.5, 2.5, 4.5]);
        let close = Series::from([4.5, 4.0, 5.0, 4.5, 5.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_hammer_bearish() {
        let open = Series::from([4.0, 5.0, 4.0, 5.0, 4.0]);
        let low = Series::from([4.5, 5.5, 4.5, 5.5, 4.5]);
        let close = Series::from([3.5, 4.0, 3.5, 4.0, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &low, &close).into();

        assert_eq!(result, expected);
    }
}
