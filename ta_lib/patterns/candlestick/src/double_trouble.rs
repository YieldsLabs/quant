use core::prelude::*;
use volatility::atr;

pub fn bullish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    let atr = atr(high, low, close, Smooth::SMMA, 10);
    let prev_close = close.shift(1);

    close.sgt(open)
        & prev_close.sgt(&open.shift(1))
        & close.sgt(&prev_close)
        & (close - open).sgt(&(2.0 * atr.shift(1)))
}

pub fn bearish(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<bool> {
    let atr = atr(high, low, close, Smooth::SMMA, 10);
    let prev_close = close.shift(1);

    close.slt(open)
        & prev_close.slt(&open.shift(1))
        & close.slt(&prev_close)
        & (open - close).sgt(&(2.0 * atr.shift(1)))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_double_trouble_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0, 4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.5, 3.5, 4.5, 3.5, 4.5, 4.5, 3.5, 4.5, 3.5, 4.5]);
        let low = Series::from([4.0, 3.0, 4.0, 3.0, 4.0, 4.0, 3.0, 4.0, 3.0, 4.0]);
        let close = Series::from([4.5, 3.5, 4.5, 3.5, 4.5, 4.5, 3.5, 4.5, 3.5, 4.5]);
        let expected = vec![
            false, false, false, false, false, false, false, false, false, false,
        ];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_double_trouble_bearish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0, 4.0, 3.0, 4.0, 3.0, 4.0]);
        let high = Series::from([4.0, 3.0, 4.0, 3.0, 4.0, 4.0, 3.0, 4.0, 3.0, 4.0]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 3.5, 3.5, 2.5, 3.5, 2.5, 3.5]);
        let close = Series::from([3.5, 2.5, 3.5, 2.5, 3.5, 3.5, 2.5, 3.5, 2.5, 3.5]);
        let expected = vec![
            false, false, false, false, false, false, false, false, false, false,
        ];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
