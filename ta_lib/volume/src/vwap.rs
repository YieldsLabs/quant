use core::series::Series;

pub fn vwap(hlc3: &[f64], volume: &[f64]) -> Series<f64> {
    let hlc3 = &Series::from(hlc3);
    let volume = &Series::from(volume);

    let product = hlc3 * volume;

    let vwap = &product.cumsum() / &volume.cumsum();

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
        let epsilon = 0.001;

        let result = vwap(&hlc3, &volume);

        for i in 0..high.len() {
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
