use core::series::Series;

pub fn rmsma(source: &[f32], period: usize) -> Series<f32> {
    let source = Series::from(source);

    let rmsma = (&source * &source).ma(period).sqrt();

    rmsma
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rmsma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![1.0, 1.5811388, 2.1602468, 3.1091263, 4.082483];

        let result: Vec<f32> = rmsma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
