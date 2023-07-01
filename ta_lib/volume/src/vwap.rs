pub fn vwap(hlc3: &[f64], volume: &[f64]) -> Vec<Option<f64>> {
    let len = hlc3.len();

    if len != volume.len() {
        return vec![None; len];
    }

    let mut vwap = vec![None; len];
    let mut sum_volume = 0.0;
    let mut vwap_numerator = 0.0;

    for i in 0..len {
        let p = hlc3[i];
        if p.is_finite() {
            sum_volume += volume[i];
            vwap_numerator += p * volume[i];
            if sum_volume != 0.0 {
                vwap[i] = Some(vwap_numerator / sum_volume);
            }
        }
    }

    vwap
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::typical::typical_price;

    #[test]
    fn test_vwap() {
        let high = vec![2.0, 4.0, 6.0];
        let low = vec![1.0, 2.0, 3.0];
        let close = vec![1.5, 3.0, 4.5];
        let volume = vec![100.0, 200.0, 300.0];
        let hlc3 = typical_price(&high, &low, &close);
        let expected = vec![Some(1.5), Some(2.5), Some(3.5)];

        let result = vwap(&hlc3, &volume);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_vwap_some_missing_values() {
        let hlc3 = vec![2.0, 4.0];
        let volume = vec![100.0, 200.0, 300.0];

        let result = vwap(&hlc3, &volume);

        assert!(result.iter().any(|r| r.is_none()));
    }
}
