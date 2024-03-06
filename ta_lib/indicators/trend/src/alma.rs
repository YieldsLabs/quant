use core::prelude::*;

pub fn alma(source: &Series<f32>, period: usize, offset: f32, sigma: f32) -> Series<f32> {
    let m = offset * (period as f32 - 1.);
    let s = period as f32 / sigma;

    let weights = (0..period)
        .map(|i| ((-1. * (i as f32 - m).powi(2)) / (2. * s.powi(2))).exp())
        .collect::<Vec<_>>();

    source.wg(&weights, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_alma() {
        let source = Series::from([
            0.01707, 0.01706, 0.01707, 0.01705, 0.01710, 0.01705, 0.01704, 0.01709,
        ]);
        let expected = [
            0.0,
            0.0,
            0.017066907,
            0.01705621,
            0.017084463,
            0.017065462,
            0.017043246,
            0.017074436,
        ];
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
