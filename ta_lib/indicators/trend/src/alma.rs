use core::prelude::*;

pub fn alma(source: &Series<f32>, period: usize, offset: f32, sigma: f32) -> Series<f32> {
    let m = (offset * (period as f32 - 1.)).floor();
    let s = period as f32 / sigma;

    let weights = (0..period)
        .rev()
        .map(|i| (-1. * (i as f32 - m).powi(2) / (2. * s.powi(2))).exp())
        .collect::<Vec<_>>();

    source.wg(&weights)
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
            0.01707,
            0.017067866,
            0.01706213,
            0.017066803,
            0.017057454,
            0.01708935,
            0.01705426,
            0.01704639,
        ];

        let result: Vec<f32> = alma(&source, 3, 0.85, 6.0).into();

        assert_eq!(result, expected);
    }
}
