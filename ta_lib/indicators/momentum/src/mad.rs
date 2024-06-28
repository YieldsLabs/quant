use core::prelude::*;

pub fn mad(source: &Series<f32>, period_fast: usize, period_slow: usize) -> Series<f32> {
    let fad = source.ma(period_fast);
    let sad = source.ma(period_slow);

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
            0.0,
            0.0,
            -0.019448167,
            -0.035259355,
            0.0619857,
            0.01336108,
            -0.0632135,
            -0.05474333,
            -0.023143804,
            -0.05484238,
            -0.015844958,
            0.023157505,
            -0.0012138351,
            -0.021954188,
            -0.002449016,
        ];
        let period_fast = 2;
        let period_slow = 3;

        let result: Vec<f32> = mad(&source, period_fast, period_slow).into();

        assert_eq!(result, expected);
    }
}
