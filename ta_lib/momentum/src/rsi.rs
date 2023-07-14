use core::series::Series;

pub fn rsi(source: &[f64], period: usize) -> Vec<f64> {
    let source = Series::from(source);
    let changes = source.change(1);

    let up = changes.max(0.0).smma(period);
    let down = changes.min(0.0).neg().smma(period);

    let rs = up / &down;

    let rsi = 100.0 - 100.0 / (1.0 + rs);

    rsi.nz(Some(100.0)).into()
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_rsi_with_valid_data() {
        let source = vec![
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ];
        let epsilon = 0.001;
        let period = 6;
        let expected = vec![
            100.0, 0.0, 22.3602, 6.5478, 56.1559, 69.602669, 74.642227, 79.480508, 84.221979,
        ];

        let result = rsi(&source, period);

        for i in 0..source.len() {
            assert!(
                (result[i] - expected[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                result[i],
                expected[i]
            )
        }
    }
}
