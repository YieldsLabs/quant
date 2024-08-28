use core::prelude::*;

const RANGE: Scalar = 0.0005;

pub fn bullish(open: &Price, low: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);
    let prev_open = open.shift(1);
    let body = (close - open).abs();
    let prev_body = body.shift(1);

    close.sgt(open)
        & low.seq(&low.shift(1))
        & body.slt(&RANGE)
        & prev_body.slt(&RANGE)
        & prev_close.slt(&prev_open)
        & close.shift(2).slt(&open.shift(1))
}

pub fn bearish(open: &Price, high: &Price, close: &Price) -> Rule {
    let prev_close = close.shift(1);
    let prev_open = open.shift(1);
    let body = (close - open).abs();
    let prev_body = body.shift(1);

    close.slt(open)
        & high.seq(&high.shift(1))
        & body.slt(&RANGE)
        & prev_body.slt(&RANGE)
        & prev_close.sgt(&prev_open)
        & close.shift(2).sgt(&open.shift(1))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tweezers_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let low = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let close = Series::from([4.5, 3.5, 4.5, 3.5, 4.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_tweezers_bearish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.0, 3.0, 4.0, 3.0, 4.0]);
        let close = Series::from([3.5, 2.5, 3.5, 2.5, 3.5]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &close).into();

        assert_eq!(result, expected);
    }
}
