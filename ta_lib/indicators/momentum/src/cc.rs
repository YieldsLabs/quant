use crate::roc;
use core::prelude::*;

pub fn cc(
    source: &Price,
    period_fast: Period,
    period_slow: Period,
    smooth: Smooth,
    period_smooth: Period,
) -> Price {
    (roc(source, period_fast) + roc(source, period_slow)).smooth(smooth, period_smooth)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cc() {
        let close = Series::from([19.299, 19.305, 19.310, 19.316, 19.347, 19.355, 19.386]);
        let expected = vec![0.0, 0.0, 0.0, 0.0, 0.0, 0.52320945, 0.6957161];

        let result: Vec<Scalar> = cc(&close, 3, 5, Smooth::WMA, 2).into();

        assert_eq!(result, expected);
    }
}
