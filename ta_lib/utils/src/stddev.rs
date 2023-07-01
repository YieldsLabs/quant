pub fn std_dev(source: &[f64], period: usize) -> Vec<Option<f64>> {
    let mut std_dev = vec![None; source.len()];
    let mut sum = 0.0;
    let mut sum_sq = 0.0;

    for (i, &value) in source.iter().enumerate() {
        sum += value;
        sum_sq += value * value;

        if i >= period {
            let old_value = source[i - period];
            sum -= old_value;
            sum_sq -= old_value * old_value;
        }

        if i + 1 >= period {
            let mean = sum / period as f64;
            let mean_sq = sum_sq / period as f64;
            std_dev[i] = Some((mean_sq - mean * mean).sqrt());
        }
    }

    std_dev
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_std_dev() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let period = 2;
        let epsilon = 0.001;
        let expected = vec![None, Some(0.5), Some(0.5), Some(0.5), Some(0.5)];

        let result = std_dev(&source, period);

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
