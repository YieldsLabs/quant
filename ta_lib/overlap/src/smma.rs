use core::series::Series;

pub fn smma(source: &[f64], period: usize) -> Series<f64> {
    let len = source.len();
    let alpha = 1.0 / (period as f64);
    let one_minus_alpha = 1.0 - alpha;

    let mut smma = Series::empty(len);

    smma[0] = Some(source[0]);

    for i in 1..len {
        let smma_prev = smma[i - 1].unwrap_or(0.0);
        smma[i] = Some(alpha * source[i] + one_minus_alpha * smma_prev);
    }

    smma
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_smma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![
            Some(1.0),
            Some(1.333),
            Some(1.888),
            Some(2.592),
            Some(3.395),
        ];
        let epsilon = 0.001;

        let result = smma(&source, 3);

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
