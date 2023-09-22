use core::Series;

pub fn vwma(source: &[f32], volume: &[f32], period: usize) -> Series<f32> {
    let source = Series::from(source);
    let volume = Series::from(volume);

    (source * &volume).ma(period) / volume.ma(period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vwma() {
        let source = vec![100.0, 105.0, 116.25, 123.125, 129.0625];
        let volume = vec![40.0, 50.0, 110.25, 90.33, 100.00];
        let period = 3;
        let expected = vec![100.0, 102.77778, 110.19507, 116.483536, 122.57867];

        let result: Vec<f32> = vwma(&source, &volume, period).into();

        assert_eq!(result, expected);
    }
}
