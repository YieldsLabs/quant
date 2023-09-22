use core::Series;

pub fn bullish(open: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    let body = (&open - &close).abs();

    close.gt(&open)
        & close.gt(&close.shift(1))
        & body.lt(&body.shift(1))
        & close.shift(1).gt(&open.shift(1))
        & close.shift(1).gt(&close.shift(2))
        & body.shift(1).lt(&body.shift(2))
        & close.shift(2).gt(&open.shift(2))
        & close.shift(2).gt(&close.shift(3))
        & body.shift(2).lt(&body.shift(3))
        & close.shift(3).gt(&open.shift(3))
        & close.shift(3).gt(&close.shift(4))
        & body.shift(3).lt(&body.shift(4))
        & close.shift(4).gt(&open.shift(4))
        & body.shift(4).lt(&body.shift(5))
}

pub fn bearish(open: &[f32], close: &[f32]) -> Series<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    let body = (&open - &close).abs();

    close.lt(&open)
        & close.lt(&close.shift(1))
        & body.lt(&body.shift(1))
        & close.shift(1).lt(&open.shift(1))
        & close.shift(1).lt(&close.shift(2))
        & body.shift(1).lt(&body.shift(2))
        & close.shift(2).lt(&open.shift(2))
        & close.shift(2).lt(&close.shift(3))
        & body.shift(2).lt(&body.shift(3))
        & close.shift(3).lt(&open.shift(3))
        & close.shift(3).lt(&close.shift(4))
        & body.shift(3).lt(&body.shift(4))
        & close.shift(4).lt(&open.shift(4))
        & body.shift(4).lt(&body.shift(5))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_quintuplets_bullish() {
        let open = vec![4.0, 4.0, 4.0, 4.0, 4.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_quintuplets_bearish() {
        let open = vec![4.0, 4.0, 4.0, 4.0, 4.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
