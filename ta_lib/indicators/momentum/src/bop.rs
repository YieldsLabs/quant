use core::prelude::*;

pub fn bop(
    open: &Price,
    high: &Price,
    low: &Price,
    close: &Price,
    smooth: Smooth,
    period_smooth: Period,
) -> Price {
    ((close - open) / (high - low)).smooth(smooth, period_smooth)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bop() {
        let open = Series::from([2.0505, 2.0310, 2.0282, 1.9937, 1.9795]);
        let high = Series::from([2.0507, 2.0310, 2.0299, 1.9977, 1.9824]);
        let low = Series::from([2.0174, 2.0208, 1.9928, 1.9792, 1.9616]);
        let close = Series::from([2.0310, 2.0282, 1.9937, 1.9795, 1.9632]);
        let expected = vec![-0.58558744, -0.4300509, -0.6022142, -0.8487407, -0.77561265];

        let result: Vec<Scalar> = bop(&open, &high, &low, &close, Smooth::SMA, 2).into();

        assert_eq!(result, expected);
    }
}
