use core::prelude::*;

const PERCENTAGE_SCALE: f32 = 100.;

pub fn chop(
    high: &Series<f32>,
    low: &Series<f32>,
    atr: &Series<f32>,
    period: usize,
) -> Series<f32> {
    PERCENTAGE_SCALE * (atr.sum(period) / (high.highest(period) - low.lowest(period))).log10()
        / (period as f32).log10()
}

#[cfg(test)]
mod tests {
    use super::*;
    use volatility::atr;

    #[test]
    fn test_chop() {
        let high = Series::from([2.0859, 2.0881, 2.0889, 2.0896, 2.0896, 2.0907]);
        let low = Series::from([2.0846, 2.0846, 2.0881, 2.0886, 2.0865, 2.0875]);
        let close = Series::from([2.0846, 2.0881, 2.0889, 2.0896, 2.0875, 2.0904]);
        let atr_period = 1;
        let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);
        let period = 2;
        let expected = [0.0, 45.571022, 0.0, 26.31491, 40.33963, 58.496246];
        let epsilon = 0.0001;

        let result: Vec<f32> = chop(&high, &low, &atr, period).into();

        for i in 0..result.len() {
            assert!(
                (result[i] - expected[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                result[i],
                expected[i]
            );
        }
    }
}
