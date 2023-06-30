use price::typical::typical_price;

pub fn vwap(high: &[f64], low: &[f64], close: &[f64], volume: &[f64]) -> Vec<Option<f64>> {
    let typical_price = typical_price(high, low, close);

    let len = typical_price.len();

    if len != volume.len() {
        return vec![None; len];
    }

    let mut vwap = vec![None; len];
    let mut sum_volume = 0.0;
    let mut vwap_numerator = 0.0;

    for i in 0..len {
        match typical_price[i] {
            Some(p) => {
                sum_volume += volume[i];
                vwap_numerator += p * volume[i];
                vwap[i] = Some(vwap_numerator / sum_volume);
            }
            None => return vec![None; len],
        }
    }

    vwap
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vwap() {
        let high = vec![2.0, 4.0, 6.0];
        let low = vec![1.0, 2.0, 3.0];
        let close = vec![1.5, 3.0, 4.5];
        let volume = vec![100.0, 200.0, 300.0];
        let expected = vec![Some(1.5), Some(2.5), Some(3.5)];

        let result = vwap(&high, &low, &close, &volume);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_vwap_some_missing_values() {
        let high = vec![2.0, 4.0, 6.0];
        let low = vec![1.0, 2.0];
        let close = vec![1.5, 3.0, 4.5];
        let volume = vec![100.0, 200.0, 300.0];

        let result = vwap(&high, &low, &close, &volume);

        assert!(result.iter().any(|r| r.is_none()));
    }
}
