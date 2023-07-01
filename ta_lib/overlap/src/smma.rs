pub fn smma(source: &[f64], period: usize) -> Vec<Option<f64>> {
    let len = source.len();

    if len < period {
        return vec![None; len];
    }

    let alpha = 1.0 / period as f64;

    let mut smma = vec![None; len];
    let mut smma_current = source[0];

    for i in 1..len {
        smma_current = (source[i] - smma_current) * alpha + smma_current;

        if i >= period - 1 {
            smma[i] = Some(smma_current);
        }
    }

    smma
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_smma_len() {
        let source = vec![1.0, 2.0];
        let result = smma(&source, 3);
        assert_eq!(source.len(), result.len());
    }

    #[test]
    fn test_smmma_edge_case() {
        let source = vec![1.0, 2.0];
        let result = smma(&source, 3);
        assert_eq!(result, vec![None, None]);
    }

    #[test]
    fn test_smma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![None, None, Some(1.888), Some(2.592), Some(3.395)];
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
