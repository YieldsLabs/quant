use overlap::smma::smma;
use utils::change::change;

pub fn rsi(source: &[f64], period: usize) -> Vec<Option<f64>> {
    let len = source.len();

    if len < period {
        return vec![None; len];
    }

    let changes = change(source, 1);

    let gains = changes.iter().map(|&x| x.max(0.0)).collect::<Vec<_>>();
    let losses = changes.iter().map(|&x| (-x).max(0.0)).collect::<Vec<_>>();

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
        let source = vec![5.0];
        let result = rsi(&source, 1);
        assert_eq!(source.len(), result.len());
    }

    #[test]
    fn test_rsi_empty() {
        let source = vec![];
        let result = rsi(&source, 14);
        assert_eq!(result, vec![]);
    }

    #[test]
    fn test_rsi_single_value() {
        let source = [10.0];
        let rsi_values = rsi(&source, 14);
        assert_eq!(rsi_values, vec![None]);
    }

    #[test]
    fn test_rsi_with_valid_data() {
        let source = vec![
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
        ];
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

        let result = rsi(&source, 6);

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
