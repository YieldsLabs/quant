use core::prelude::*;

pub fn vwema(source: &Series<f32>, volume: &Series<f32>, period: usize) -> Series<f32> {
    (source * volume).smooth(Smooth::EMA, period) / volume.smooth(Smooth::EMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vwema() {
        let source = Series::from([100.0, 105.0, 116.25, 123.125, 129.0625]);
        let volume = Series::from([40.0, 50.0, 110.25, 90.33, 100.00]);
        let period = 3;
        let expected = vec![100.0, 102.77778, 112.34501, 118.14274, 124.07811];

        let result: Vec<f32> = vwema(&source, &volume, period).into();

        assert_eq!(result, expected);
    }
}
