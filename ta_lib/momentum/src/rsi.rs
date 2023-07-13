use core::series::Series;
use overlap::smma::smma;

pub fn rsi(source: &[f64], period: usize) -> Series<f64> {
    let source = Series::from(source);
    let changes = source.change(1);

    let gains: Vec<f64> = changes.max(0.0).into();
    let losses: Vec<f64> = changes.min(0.0).neg().into();

    let up = smma(&gains, period);
    let down = smma(&losses, period);

    let rs = &up / &down;

    let rsi = 100.0 - &(100.0 / &(1.0 + &rs));

    rsi.nz(Some(100.0))
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
            Some(100.0),
            Some(0.0),
            Some(22.3602),
            Some(6.5478),
            Some(56.1559),
            Some(69.602669),
            Some(74.642227),
            Some(79.480508),
            Some(84.221979),
        ];

        let result = rsi(&source, period);

        for i in 0..source.len() {
            match (result[i], expected[i]) {
                (Some(a), Some(b)) => {
                    assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b)
                }
                (None, None) => {}
                _ => panic!("at position {}: {:?} != {:?}", i, result[i], expected[i]),
            }
        }
    }
}
