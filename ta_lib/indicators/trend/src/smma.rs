use core::prelude::*;

pub fn smma(source: &Series<f32>, period: usize) -> Series<f32> {
    source.smma(period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_smma() {
        let source = Series::from([
            6.8575, 6.855, 6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365,
            6.8310, 6.8355, 6.8360, 6.8345, 6.8285, 6.8395,
        ]);
        let expected = [
            6.8575, 6.8566666, 6.857111, 6.8580737, 6.8547153, 6.8556433, 6.8584285, 6.857785,
            6.85369, 6.8507934, 6.846029, 6.8410187, 6.839179, 6.8381195, 6.8369126, 6.8341084,
            6.835905,
        ];

        let result: Vec<f32> = smma(&source, 3).into();

        assert_eq!(result, expected)
    }
}
