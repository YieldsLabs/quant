use core::prelude::*;

pub fn ema(source: &Series<f32>, period: usize) -> Series<f32> {
    source.ema(period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ema() {
        let source = Series::from([
            6.8575, 6.855, 6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365,
            6.8310, 6.8355, 6.8360, 6.8345, 6.8285, 6.8395,
        ]);
        let expected = vec![
            6.8575, 6.85625, 6.857125, 6.8585625, 6.853281, 6.8553905, 6.8596954, 6.858098,
            6.851799, 6.848399, 6.8424497, 6.8367248, 6.836112, 6.8360558, 6.8352776, 6.8318887,
            6.8356943,
        ];

        let result: Vec<f32> = ema(&source, 3).into();

        assert_eq!(result, expected);
    }
}
