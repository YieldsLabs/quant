use core::prelude::*;

pub fn vwap(source: &Series<f32>, volume: &Series<f32>) -> Series<f32> {
    (source * volume).cumsum() / volume.cumsum()
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::prelude::*;

    #[test]
    fn test_vwap() {
        let high = Series::from([2.0, 4.0, 6.0]);
        let low = Series::from([1.0, 2.0, 3.0]);
        let close = Series::from([1.5, 3.0, 4.5]);
        let volume = Series::from([100.0, 200.0, 300.0]);
        let hlc3 = typical_price(&high, &low, &close);
        let expected = [1.5, 2.5, 3.5];
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
