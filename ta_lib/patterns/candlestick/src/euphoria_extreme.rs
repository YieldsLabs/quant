use core::prelude::*;

pub fn bullish(open: &Price, close: &Price) -> Rule {
    let body = (close - open).abs();

    let back_2_body = body.shift(2);
    let back_3_body = body.shift(3);

    close.shift(5).slt(&open.shift(5))
        & close.shift(4).slt(&open.shift(4))
        & close.shift(3).slt(&open.shift(3))
        & close.shift(2).slt(&open.shift(2))
        & close.shift(1).slt(&open.shift(1))
        & body.shift(1).sgt(&back_2_body)
        & back_2_body.sgt(&back_3_body)
        & back_3_body.sgt(&body.shift(4))
}

pub fn bearish(open: &Price, close: &Price) -> Rule {
    let body = (close - open).abs();

    let back_2_body = body.shift(2);
    let back_3_body = body.shift(3);

    close.shift(5).sgt(&open.shift(5))
        & close.shift(4).sgt(&open.shift(4))
        & close.shift(3).sgt(&open.shift(3))
        & close.shift(2).slt(&open.shift(2))
        & close.shift(1).slt(&open.shift(1))
        & body.shift(1).sgt(&back_2_body)
        & back_2_body.sgt(&back_3_body)
        & back_3_body.sgt(&body.shift(4))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_euphoria_extreme_bullish() {
        let open = Series::from([4.0, 4.0, 4.0, 4.0, 5.0]);
        let close = Series::from([5.0, 3.0, 4.0, 4.0, 6.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_euphoria_extreme_bearish() {
        let open = Series::from([4.0, 4.0, 4.0, 6.0, 5.0]);
        let close = Series::from([5.0, 5.0, 4.0, 6.0, 4.0]);
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
