use crate::roc;
use core::prelude::*;

pub fn kst(
    source: &Series<f32>,
    roc_period_first: usize,
    roc_period_second: usize,
    roc_period_third: usize,
    roc_period_fouth: usize,
    period_first: usize,
    period_second: usize,
    period_third: usize,
    period_fouth: usize,
) -> Series<f32> {
    roc(source, roc_period_first).ma(period_first)
        + (2. * roc(source, roc_period_second).ma(period_second))
        + (3. * roc(source, roc_period_third).ma(period_third))
        + (4. * roc(source, roc_period_fouth).ma(period_fouth))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kst() {
        let source = Series::from([
            2.0752, 2.0781, 2.0716, 2.0766, 2.0848, 2.0931, 2.0967, 2.1024, 2.1060, 2.1075, 2.1146,
            2.1145,
        ]);
        let roc_period_one = 2;
        let roc_period_two = 3;
        let roc_period_three = 4;
        let roc_period_four = 5;
        let period_one = 2;
        let period_two = 3;
        let period_three = 4;
        let period_four = 5;

        let expected = vec![
            0.0,
            0.0,
            -0.08674153,
            -0.07785419,
            0.8893757,
            3.2460651,
            5.4379296,
            7.731903,
            8.935576,
            9.378514,
            9.048229,
            8.414183,
        ];

        let result: Vec<f32> = kst(
            &source,
            roc_period_one,
            roc_period_two,
            roc_period_three,
            roc_period_four,
            period_one,
            period_two,
            period_three,
            period_four,
        )
        .into();

        assert_eq!(result, expected);
    }
}
