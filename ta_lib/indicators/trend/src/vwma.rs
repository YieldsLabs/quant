use core::prelude::*;

pub fn vwma(source: &Series<f32>, volume: &Series<f32>, period: usize) -> Series<f32> {
    (source * volume).smooth(Smooth::SMA, period) / volume.smooth(Smooth::SMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vwma() {
        let source = Series::from([100.0, 105.0, 116.25, 123.125, 129.0625]);
        let volume = Series::from([40.0, 50.0, 110.25, 90.33, 100.00]);
        let period = 3;
        let expected = vec![100.0, 102.77778, 110.19507, 116.483536, 122.57867];

        let result: Vec<f32> = vwma(&source, &volume, period).into();

        assert_eq!(result, expected);
    }
}
