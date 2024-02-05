use core::prelude::*;

pub fn cci(source: &Series<f32>, smooth_type: Smooth, period: usize, factor: f32) -> Series<f32> {
    (source - source.smooth(smooth_type, period)) / (factor * source.mad(period))
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::prelude::*;

    #[test]
    fn test_cci() {
        let high = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let low = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let close = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let hlc3 = typical_price(&high, &low, &close);
        let expected = vec![0.0, 66.66667, 100.0, 100.0, 100.0];

        let result: Vec<f32> = cci(&hlc3, Smooth::SMA, 3, 0.015).into();

        assert_eq!(result, expected);
    }
}
