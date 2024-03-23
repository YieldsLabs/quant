use core::prelude::*;

pub fn stoch(
    source: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    period: usize,
) -> Series<f32> {
    let hh = high.highest(period);
    let ll = low.lowest(period);

    SCALE * (source - &ll) / (hh - ll)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stoch() {
        let high = Series::from([3.0, 3.0, 3.0, 3.0, 3.0]);
        let low = Series::from([1.0, 1.0, 1.0, 1.0, 1.0]);
        let source = Series::from([2.0, 2.5, 2.0, 1.5, 2.0]);
        let period = 3;

        let expected = vec![50.0, 75.0, 50.0, 25.0, 50.0];

        let result: Vec<f32> = stoch(&source, &high, &low, period).into();

        assert_eq!(result, expected);
    }
}
