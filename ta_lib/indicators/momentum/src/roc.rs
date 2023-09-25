use core::Series;

pub fn roc(source: &Series<f32>, period: usize) -> Series<f32> {
    100.0 * source.change(period) / source.shift(period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_roc() {
        let source = Series::from([19.310, 19.316, 19.347, 19.355, 19.386]);
        let period = 3;
        let expected = vec![0.0, 0.0, 0.0, 0.23304027, 0.36239228];

        let result: Vec<f32> = roc(&source, period).into();

        assert_eq!(result, expected);
    }
}
