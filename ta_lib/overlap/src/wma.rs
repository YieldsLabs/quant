pub fn wma(source: &[f64], period: usize) -> Vec<Option<f64>> {
    let len = source.len();

    if len < period {
        return vec![None; len];
    }

    let mut wma = vec![None; len];
    let weight_sum = (period * (period + 1)) as f64 / 2.0;

    let mut sum = 0.0;

    for i in 0..period {
        let weight = (i + 1) as f64;
        let value = source[i];
        sum += value * weight;
    }

    wma[period - 1] = Some(sum / weight_sum);

    for i in period..len {
        sum = sum + (source[i] - source[i - period]) * period as f64 - (weight_sum - period as f64);
        wma[i] = Some(sum / weight_sum);
    }

    wma
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_wma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let period = 3;
        let epsilon = 0.001;
        let expected = vec![None, None, Some(2.333333), Some(3.333333), Some(4.333333)];

        let result = wma(&source, period);

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
