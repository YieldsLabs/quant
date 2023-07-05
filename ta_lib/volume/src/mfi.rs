use utils::change::change;

pub fn mfi(hlc3: &[f64], volume: &[f64], period: usize) -> Vec<Option<f64>> {
    let len = hlc3.len();
    let mut mfi = vec![None; len];

    if len < period || len != volume.len() {
        return mfi;
    }

    let changes = change(hlc3, 1);
    let mut upper = 0.0;
    let mut lower = 0.0;

    for i in 0..period {
        if changes[i] < 0.0 {
            lower += volume[i] * hlc3[i];
        }

        if changes[i] > 0.0 {
            upper += volume[i] * hlc3[i];
        }
    }

    mfi[period - 1] = Some(100.0 - (100.0 / (1.0 + upper / (lower + std::f64::EPSILON))));

    for i in period..len {
        if changes[i - period] < 0.0 {
            lower -= volume[i - period] * hlc3[i - period];
        }

        if changes[i - period] > 0.0 {
            upper -= volume[i - period] * hlc3[i - period];
        }

        if changes[i] < 0.0 {
            lower += volume[i] * hlc3[i];
        }

        if changes[i] > 0.0 {
            upper += volume[i] * hlc3[i];
        }

        mfi[i] = Some(100.0 - (100.0 / (1.0 + upper / (lower + std::f64::EPSILON))));
    }

    mfi
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mfi() {
        let hlc3 = vec![2.0, 2.1666, 2.0, 1.8333, 2.0];
        let volume = vec![1.0, 1.0, 1.0, 1.0, 1.0];
        let period = 3;
        let epsilon = 0.001;

        let expected = vec![None, None, Some(51.9992), Some(36.1106), Some(34.2859)];

        let result = mfi(&hlc3, &volume, period);

        for i in 0..hlc3.len() {
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
