use core::series::Series;

pub fn tema(source: &[f32], period: usize) -> Series<f32> {
    let source = Series::from(source);

    let ema1 = source.ema(period);
    let ema2 = ema1.ema(period);
    let ema3 = ema2.ema(period);

    3.0 * (ema1 - ema2) + ema3
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tema() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![1.0, 1.875, 2.9375, 4.0, 5.03125];

        let result: Vec<f32> = tema(&source, 3).into();

        assert_eq!(result, expected);
    }
}
