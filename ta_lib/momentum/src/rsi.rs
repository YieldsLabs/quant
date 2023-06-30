use overlap::smma::smma;

pub fn rsi(data: &[f64], period: usize) -> Vec<Option<f64>> {
    let len = data.len();

    if len < period {
        return vec![None; len];
    }

    let mut gains = vec![0.0; len];
    let mut losses = vec![0.0; len];

    for i in 1..data.len() {
        let change = data[i] - data[i - 1];

        gains[i] = change.max(0.0);
        losses[i] = (-change).max(0.0);
    }

    let avg_gain = smma(&gains, period);
    let avg_loss = smma(&losses, period);

    let rsi = avg_gain
        .iter()
        .zip(&avg_loss)
        .map(|(&gain, &loss)| match (gain, loss) {
            (Some(gain), Some(loss)) if gain + loss > 0.0 => {
                let rs = gain / (loss + std::f64::EPSILON);
                Some(100.0 - (100.0 / (1.0 + rs)))
            }
            _ => None,
        })
        .collect();

    rsi
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_rsi_len() {
        let data = vec![5.0];
        let result = rsi(&data, 1);
        assert_eq!(data.len(), result.len());
    }

    #[test]
    fn test_rsi_empty() {
        let data = vec![];
        let result = rsi(&data, 14);
        assert_eq!(result, vec![]);
    }

    #[test]
    fn test_rsi_single_value() {
        let data = [10.0];
        let rsi_values = rsi(&data, 14);
        assert_eq!(rsi_values, vec![None]);
    }

    #[test]
    fn test_rsi_with_valid_data() {
        let data = vec![
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ];
        let result = rsi(&data, 6);
        let epsilon = 0.001;
        let expected = vec![
            None,
            None,
            None,
            None,
            None,
            Some(69.602669),
            Some(74.642227),
            Some(79.480508),
            Some(84.221979),
        ];

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
