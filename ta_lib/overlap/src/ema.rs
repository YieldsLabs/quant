pub fn ema(data: &[f64], period: usize) -> Vec<Option<f64>> {
    let len = data.len();

    if len < period {
        return vec![None; len];
    }

    let alpha = 2.0 / (period as f64 + 1.0);

    let mut ema = vec![None; len];
    let mut ema_current = data[0];

    for i in 1..len {
        ema_current = (data[i] - ema_current) * alpha + ema_current;

        if i >= period - 1 {
            ema[i] = Some(ema_current);
        }
    }

    ema
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ema_len() {
        let data = vec![1.0, 2.0];
        let result = ema(&data, 3);
        assert_eq!(data.len(), result.len());
    }

    #[test]
    fn test_ema_edge_case() {
        let data = vec![1.0, 2.0];
        let result = ema(&data, 3);
        assert_eq!(result, vec![None, None]);
    }

    #[test]
    fn test_ema() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let result = ema(&data, 3);
        assert_eq!(
            result,
            vec![None, None, Some(2.25), Some(3.125), Some(4.0625)]
        );
    }
}
