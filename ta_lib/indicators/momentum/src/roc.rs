use core::Series;

pub fn roc(source: &Series<f32>, period: usize) -> Series<f32> {
    100.0 * source.change(period) / source.shift(period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_roc() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let period = 3;
        let expected = vec![0.0, 0.0, 0.0, 300.0, 150.0];

        let result: Vec<f32> = roc(&source, period).into();

        assert_eq!(result, expected);
    }
}
