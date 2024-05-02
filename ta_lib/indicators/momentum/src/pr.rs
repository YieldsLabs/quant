use core::prelude::*;

pub fn pr(
    source: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    period: usize,
) -> Series<f32> {
    let hh = high.highest(period);
    let ll = low.lowest(period);

    SCALE * (source - &hh) / (&hh - &ll)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pr() {
        let high = Series::from([6.748, 6.838, 6.804, 6.782, 6.786]);
        let low = Series::from([6.655, 6.728, 6.729, 6.718, 6.732]);
        let source = Series::from([6.738, 6.780, 6.751, 6.766, 6.735]);
        let period = 3;

        let expected = vec![-10.752942, -31.693844, -47.541027, -60.00008, -80.23232];

        let result: Vec<f32> = pr(&source, &high, &low, period).into();

        assert_eq!(result, expected);
    }
}
