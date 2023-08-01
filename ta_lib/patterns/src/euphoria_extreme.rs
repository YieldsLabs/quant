use core::series::Series;

pub fn bullish(open: &[f64], close: &[f64]) -> Vec<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    let body = (&close - &open).abs();

    (close.shift(5).lt(&open.shift(5))
        & close.shift(4).lt(&open.shift(4))
        & close.shift(3).lt(&open.shift(3))
        & close.shift(2).lt(&open.shift(2))
        & close.shift(1).lt(&open.shift(1))
        & body.shift(1).gt(&body.shift(2))
        & body.shift(2).gt(&body.shift(3))
        & body.shift(3).gt(&body.shift(4)))
    .into()
}

pub fn bearish(open: &[f64], close: &[f64]) -> Vec<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    let body = (&close - &open).abs();

    (close.shift(5).gt(&open.shift(5))
        & close.shift(4).gt(&open.shift(4))
        & close.shift(3).gt(&open.shift(3))
        & close.shift(2).lt(&open.shift(2))
        & close.shift(1).lt(&open.shift(1))
        & body.shift(1).gt(&body.shift(2))
        & body.shift(2).gt(&body.shift(3))
        & body.shift(3).gt(&body.shift(4)))
    .into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_euphoria_extreme_bullish() {
        let open = vec![4.0, 4.0, 4.0, 4.0, 5.0];
        let close = vec![5.0, 3.0, 4.0, 4.0, 6.0];
        let expected = vec![false, false, false, false, false];

        let result = bullish(&open, &close);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_euphoria_extreme_bearish() {
        let open = vec![4.0, 4.0, 4.0, 6.0, 5.0];
        let close = vec![5.0, 5.0, 4.0, 6.0, 4.0];
        let expected = vec![false, false, false, false, false];

        let result = bearish(&open, &close);

        assert_eq!(result, expected);
    }
}
