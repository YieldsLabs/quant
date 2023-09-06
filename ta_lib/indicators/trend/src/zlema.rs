use core::series::Series;

pub fn zlema(source: &[f32], period: usize) -> Series<f32> {
    let source = Series::from(source);
    let lag = (period as f32 / 2.0).round() as usize;

    let d = (2.0 * &source) - source.shift(lag);
    let zlema = d.ema(period);

    zlema
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zlema() {
        let source = vec![100.0, 105.0, 116.25, 123.125, 129.0625];
        let period = 3;
        let expected = vec![0.0, 0.0, 132.5, 136.875, 139.375];

        let result: Vec<f32> = zlema(&source, period).into();

        assert_eq!(result, expected);
    }
}
