use core::prelude::*;

pub fn bullish(open: &Price, high: &Price, low: &Price, close: &Price) -> Rule {
    let back_6_high = high.shift(6);
    let back_6_low = low.shift(6);

    close.sgt(&back_6_high)
        & close.sgt(open)
        & high.shift(1).slt(&back_6_high)
        & low.shift(1).sgt(&back_6_low)
        & high.shift(2).slt(&back_6_high)
        & low.shift(2).sgt(&back_6_low)
        & high.shift(3).slt(&back_6_high)
        & low.shift(3).sgt(&back_6_low)
        & high.shift(4).slt(&back_6_high)
        & low.shift(4).sgt(&back_6_low)
        & high.shift(5).slt(&back_6_high)
        & low.shift(5).sgt(&back_6_low)
}

pub fn bearish(open: &Price, high: &Price, low: &Price, close: &Price) -> Rule {
    let back_6_high = high.shift(6);
    let back_6_low = low.shift(6);

    close.slt(&back_6_low)
        & close.slt(open)
        & high.shift(1).slt(&back_6_high)
        & low.shift(1).sgt(&back_6_low)
        & high.shift(2).slt(&back_6_high)
        & low.shift(2).sgt(&back_6_low)
        & high.shift(3).slt(&back_6_high)
        & low.shift(3).sgt(&back_6_low)
        & high.shift(4).slt(&back_6_high)
        & low.shift(4).sgt(&back_6_low)
        & high.shift(5).slt(&back_6_high)
        & low.shift(5).sgt(&back_6_low)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_master_candle_bullish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0, 6.0]);
        let high = Series::from([4.5, 3.5, 4.5, 3.5, 4.5, 5.0]);
        let low = Series::from([4.0, 3.0, 4.0, 3.0, 4.0, 3.6]);
        let close = Series::from([4.5, 3.5, 4.5, 3.5, 4.5, 4.5]);
        let expected = vec![false, false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_master_candle_bearish() {
        let open = Series::from([4.0, 3.0, 4.0, 3.0, 4.0, 6.0]);
        let high = Series::from([4.0, 3.0, 4.0, 3.0, 4.0, 5.0]);
        let low = Series::from([3.5, 2.5, 3.5, 2.5, 3.5, 3.4]);
        let close = Series::from([3.5, 2.5, 3.5, 2.5, 3.5, 5.6]);
        let expected = vec![false, false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
