use core::prelude::*;

pub fn eom(
    hl2: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    volume: &Series<f32>,
    period: usize,
    divisor: f32,
) -> Series<f32> {
    (divisor * hl2.change(1) * (high - low) / volume).ma(period)
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::median_price;

    #[test]
    fn test_eom() {
        let high = Series::from([2.0859, 2.0881, 2.0889, 2.0896, 2.0896, 2.0907]);
        let low = Series::from([2.0846, 2.0846, 2.0881, 2.0886, 2.0865, 2.0875]);

        let volume = Series::from([528.0, 69.0, 136.0, 78.0, 353.0, 59.0]);

        let expected = [
            0.0,
            0.00027900035,
            0.00034224786,
            0.00010170654,
            -0.000007647926,
            0.00023862119,
        ];

        let hlc = median_price(&high, &low);
        let period = 2;
        let divisor = 10000.0;

        let result: Vec<f32> = eom(&hlc, &high, &low, &volume, period, divisor).into();

        assert_eq!(result, expected);
    }
}
