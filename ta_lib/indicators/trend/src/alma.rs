use core::series::Series;

pub fn alma(source: &[f32], period: usize, offset: f32, sigma: f32) -> Series<f32> {
    let source = Series::from(source);

    let alma = source.alma(period, offset, sigma);

    alma
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_alma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![0.0, 0.0, 2.6856735, 3.6856737, 4.685674];

        let result: Vec<f32> = alma(&source, 3, 0.85, 6.0).into();

        assert_eq!(result, expected);
    }
}
