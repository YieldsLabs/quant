pub fn sma(source: &[f64], period: usize) -> Vec<Option<f64>> {
    let len = source.len();

    if len < period {
        return vec![None; len];
    }

    let mut sma = vec![None; len];
    let mut sum = 0.0;

    for i in 0..len {
        sum += source[i];

        if i >= period {
            sum -= source[i - period];
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
        let source = vec![1.0, 2.0];
        let result = sma(&source, 3);
        assert_eq!(source.len(), result.len());
    }

    #[test]
    fn test_sma_edge_case() {
        let source = vec![1.0, 2.0];
        let result = sma(&source, 3);
        assert_eq!(result, vec![None, None]);
    }

    #[test]
    fn test_sma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = sma(&source, 3);
        assert_eq!(result, vec![None, None, Some(2.0), Some(3.0), Some(4.0)]);
    }
}
