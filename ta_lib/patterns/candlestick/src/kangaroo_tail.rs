use core::series::Series;

pub fn bullish(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    let range = &high - &low;
    let two_third_low_range = &range * 0.66 + &low;

    close.gt(&two_third_low_range)
        & open.gt(&two_third_low_range)
        & close.gt(&low.shift(1))
        & close.lt(&high.shift(1))
        & open.gt(&low.shift(1))
        & open.lt(&high.shift(1))
        & close.lt(&close.shift(200))
        & range.gt(&range.shift(1))
        & range.gt(&range.shift(2))
        & range.gt(&range.shift(3))
        & close.shift(1).lt(&open.shift(2))
        & low.lte(&low.lowest(13))
}

pub fn bearish(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    let range = &high - &low;
    let two_third_high_range = &high - &range * 0.66;

    close.lt(&two_third_high_range)
        & open.lt(&two_third_high_range)
        & close.gt(&low.shift(1))
        & close.lt(&high.shift(1))
        & open.gt(&low.shift(1))
        & open.lt(&high.shift(1))
        & close.gt(&close.shift(200))
        & range.gt(&range.shift(1))
        & range.gt(&range.shift(2))
        & range.gt(&range.shift(3))
        & close.shift(1).gt(&open.shift(2))
        & high.lte(&high.lowest(13))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kangaroo_tail_bullish() {
        let open = vec![4.0; 201];
        let high = vec![4.5; 201];
        let low = vec![4.0; 201];
        let close = vec![4.5; 201];
        let expected = vec![false; 201];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_kangaroo_tail_bearish() {
        let open = vec![4.0; 201];
        let high = vec![4.5; 201];
        let low = vec![4.0; 201];
        let close = vec![4.5; 201];
        let expected = vec![false; 201];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
