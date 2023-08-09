use core::series::Series;

pub fn vwap(hlc3: &[f32], volume: &[f32]) -> Series<f32> {
    let hlc3 = Series::from(hlc3);
    let volume = Series::from(volume);

    let product = hlc3 * &volume;

    let vwap = product.cumsum() / volume.cumsum();

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
        let expected = vec![1.5, 2.5, 3.5];
        let epsilon = 0.001;

        let result: Vec<f32> = vwap(&hlc3, &volume).into();

        for i in 0..high.len() {
            assert!(
                (result[i] - expected[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                result[i],
                expected[i]
            )
        }
    }
}
