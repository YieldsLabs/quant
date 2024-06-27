use core::prelude::*;

pub fn mad(source: &Series<f32>, period_fast: usize, period_slow: usize) -> Series<f32> {
    let fad = source.ad(period_fast);
    let sad = source.ad(period_slow);

    SCALE * (fad - &sad) / &sad
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mad() {
        let source = Series::from([
            6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365, 6.8310, 6.8355,
            6.8360, 6.8345, 6.8285, 6.8395,
        ]);
        let expected = vec![
            0.0, 0.0, -18.180635, 103.59698, -56.669632, 32.346012, -44.06944, -93.74106,
            -27.147879, -57.692024, 92.80752, -86.342354, -9.959931, -33.333332, 3.138412,
        ];
        let period_fast = 2;
        let period_slow = 3;

        let result: Vec<f32> = mad(&source, period_fast, period_slow).into();

        assert_eq!(result, expected);
    }
}
