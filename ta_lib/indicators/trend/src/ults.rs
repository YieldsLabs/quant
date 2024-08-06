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
        let expected = vec![18.898, 18.85439, 18.853537, 18.922752, 18.880928];

        let result: Vec<f32> = ults(&source, period).into();

        assert_eq!(result, expected);
    }
}
