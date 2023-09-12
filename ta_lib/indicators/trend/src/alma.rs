use core::series::Series;

pub fn alma(source: &[f32], period: usize, offset: f32, sigma: f32) -> Series<f32> {
    let source = Series::from(source);

    let m = offset * (period as f32 - 1.0);
    let s = period as f32 / sigma;

    let len = source.len();
    let mut sum = Series::empty(len).nz(Some(0.0));
    let mut norm = 0.0;

    for i in 0..period {
        let weight = ((-1.0 * (i as f32 - m).powi(2)) / (2.0 * s.powi(2))).exp();

        norm += weight;
        sum = sum + source.shift(period - i - 1) * weight;
    }

    sum / norm
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
