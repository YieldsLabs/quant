use core::prelude::*;

pub fn alma(source: &Series<f32>, period: usize, offset: f32, sigma: f32) -> Series<f32> {
    let m = offset * (period as f32 - 1.);
    let s = period as f32 / sigma;

    let mut sum = Series::zero(source.len());
    let mut norm = 0.;

    for i in 0..period {
        let weight = ((-1. * (i as f32 - m).powi(2)) / (2. * s.powi(2))).exp();

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
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = [0.0, 0.0, 2.6856735, 3.6856735, 4.6856737];
        let epsilon = 0.001;

        let result: Vec<f32> = alma(&source, 3, 0.85, 6.0).into();

        for i in 0..source.len() {
            assert!(
                (result[i] - expected[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                result[i],
                expected[i]
            );
        }
    }
}
