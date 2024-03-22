use core::prelude::*;

pub fn vidya(source: &Series<f32>, short_period: usize, long_period: usize) -> Series<f32> {
    let alpha =
        2. / (short_period as f32 + 1.) * source.std(short_period) / source.std(long_period);

    source.ew(&alpha, source)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vidya() {
        let source = Series::from([100.0, 105.0, 116.25, 123.125, 129.0625]);
        let short_period = 2;
        let long_period = 3;
        let expected = vec![100.0, 103.33333, 110.46114, 114.34566, 119.90917];

        let result: Vec<f32> = vidya(&source, short_period, long_period).into();

        assert_eq!(result, expected);
    }
}
