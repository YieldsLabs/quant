use core::series::Series;
use volatility::atr::atr;

pub fn bullish(open: &[f32], high: &[f32], low: &[f32], close: &[f32]) -> Series<bool> {
    let atr = atr(high, low, close, 10, None);
    let open = Series::from(open);
    let close = Series::from(close);

    close.gt(&open)
        & close.shift(1).gt(&open.shift(1))
        & close.gt(&close.shift(1))
        & (&close - &open).gt(&(2.0 * atr.shift(1)))
}

pub fn bearish(open: &[f32], high: &[f32], low: &[f32], close: &[f32]) -> Series<bool> {
    let atr = atr(high, low, close, 10, None);
    let open = Series::from(open);
    let close = Series::from(close);

    close.lt(&open)
        & close.shift(1).lt(&open.shift(1))
        & close.lt(&close.shift(1))
        & (&open - &close).gt(&(2.0 * atr.shift(1)))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_double_trouble_bullish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0, 4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.5, 3.5, 4.5, 3.5, 4.5, 4.5, 3.5, 4.5, 3.5, 4.5];
        let low = vec![4.0, 3.0, 4.0, 3.0, 4.0, 4.0, 3.0, 4.0, 3.0, 4.0];
        let close = vec![4.5, 3.5, 4.5, 3.5, 4.5, 4.5, 3.5, 4.5, 3.5, 4.5];
        let expected = vec![
            false, false, true, false, false, false, false, false, false, false,
        ];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_double_trouble_bearish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0, 4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.0, 3.0, 4.0, 3.0, 4.0, 4.0, 3.0, 4.0, 3.0, 4.0];
        let low = vec![3.5, 2.5, 3.5, 2.5, 3.5, 3.5, 2.5, 3.5, 2.5, 3.5];
        let close = vec![3.5, 2.5, 3.5, 2.5, 3.5, 3.5, 2.5, 3.5, 2.5, 3.5];
        let expected = vec![
            false, true, false, true, false, false, false, false, false, false,
        ];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
