pub fn smma(data: &[f64], period: usize) -> Vec<Option<f64>> {
    if data.len() < period {
        return vec![None; data.len()];
    }

    let alpha = 1.0 / period as f64;

    let mut smma = vec![None; data.len()];

    let mut smma_current = data[0];

    for i in 1..data.len() {
        smma_current = (data[i] - smma_current) * alpha + smma_current;
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
        let data = vec![1.0, 2.0];
        let result = smma(&data, 3);
        assert_eq!(data.len(), result.len());
    }

    #[test]
    fn test_smmma_edge_case() {
        let data = vec![1.0, 2.0];
        let result = smma(&data, 3);
        assert_eq!(result, vec![None, None]);
    }

    #[test]
    fn test_smma() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = smma(&data, 3);
        let expected = vec![None, None, Some(1.888), Some(2.592), Some(3.395)];
        let epsilon = 0.001;

        for i in 0..result.len() {
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
