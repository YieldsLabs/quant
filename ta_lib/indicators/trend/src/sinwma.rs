use core::Series;
use std::f32::consts::PI;

pub fn sinwma(source: &[f32], period: usize) -> Series<f32> {
    let source = Series::from(source);

    let mut sum = Series::zero(source.len());
    let mut norm = 0.0;

    for i in 0..period {
        let weight = ((i + 1) as f32 / period as f32 * (PI / 2.0)).sin();

        norm += weight;
        sum = sum + source.shift(period - i - 1) * weight;
    }

    sum / norm
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sinwma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![0.0, 0.0, 2.211325, 3.211325, 4.2113247];

        let result: Vec<f32> = sinwma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
