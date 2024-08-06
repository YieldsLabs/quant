use core::prelude::*;

pub fn zlema(source: &Series<f32>, period: usize) -> Series<f32> {
    source.smooth(Smooth::ZLEMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zlema() {
        let source = Series::from([18.898, 18.838, 18.881, 18.925, 18.846]);
        let period = 3;
        let expected = vec![18.898, 18.838, 18.881, 18.925, 18.846];

        let result: Vec<f32> = zlema(&source, period).into();

        assert_eq!(result, expected);
    }
}
