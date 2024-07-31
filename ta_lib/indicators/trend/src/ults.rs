use core::prelude::*;

pub fn ults(source: &Series<f32>, period: usize) -> Series<f32> {
    source.smooth(Smooth::ULTS, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ults() {
        let source = Series::from([18.898, 18.838, 18.881, 18.925, 18.846]);
        let period = 3;
        let expected = vec![0.0, 0.0, 18.852865, 18.924725, 18.879599];

        let result: Vec<f32> = ults(&source, period).into();

        assert_eq!(result, expected);
    }
}
