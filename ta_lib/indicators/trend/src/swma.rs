use core::series::Series;

pub fn swma(source: &[f32]) -> Series<f32> {
    let source = Series::from(source);

    let x1 = source.shift(1);
    let x2 = source.shift(2);
    let x3 = source.shift(3);

    x3 * 1.0 / 6.0 + x2 * 2.0 / 6.0 + x1 * 2.0 / 6.0 + source * 1.0 / 6.0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_swma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![0.0, 0.0, 0.0, 2.5, 3.5];

        let result: Vec<f32> = swma(&source).into();

        assert_eq!(result, expected);
    }
}
