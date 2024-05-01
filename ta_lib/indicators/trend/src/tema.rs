use core::prelude::*;

pub fn tema(source: &Series<f32>, period: usize) -> Series<f32> {
    source.smooth(Smooth::TEMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tema() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = vec![1.0, 1.875, 2.9375, 4.0, 5.03125];

        let result: Vec<f32> = tema(&source, 3).into();

        assert_eq!(result, expected);
    }
}
