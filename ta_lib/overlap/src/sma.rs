pub fn sma(data: &[f64], period: usize) -> Vec<Option<f64>> {
    let mut sma = vec![None; data.len()];
    let mut sum = 0.0;

    for i in 0..data.len() {
        sum += data[i];

        if i >= period {
            sum -= data[i - period];
            sma[i] = Some(sum / period as f64);
        } else if i + 1 == period {
            sma[i] = Some(sum / period as f64);
        }
    }

    sma
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sma_len() {
        let data = vec![1.0, 2.0];
        let result = sma(&data, 3);
        assert_eq!(data.len(), result.len());
    }

    #[test]
    fn test_sma_edge_case() {
        let data = vec![1.0, 2.0];
        let result = sma(&data, 3);
        assert_eq!(result, vec![None, None]);
    }

    #[test]
    fn test_sma() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = sma(&data, 3);
        assert_eq!(result, vec![None, None, Some(2.0), Some(3.0), Some(4.0)]);
    }
}
