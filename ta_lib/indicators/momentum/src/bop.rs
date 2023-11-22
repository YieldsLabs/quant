use core::Series;

pub fn bop(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> Series<f32> {
    (close - open) / (high - low)
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
        let expected = vec![-0.58558744, -0.27451438, -0.92991406, -0.7675673, -0.783658];

        let result: Vec<f32> = bop(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
