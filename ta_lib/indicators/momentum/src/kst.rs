use crate::roc;
use core::prelude::*;

pub fn kst(
    source: &Price,
    smooth: Smooth,
    period_roc_first: Period,
    period_roc_second: Period,
    period_roc_third: Period,
    period_roc_fouth: Period,
    period_first: Period,
    period_second: Period,
    period_third: Period,
    period_fouth: Period,
) -> Price {
    roc(source, period_roc_first).smooth(smooth, period_first)
        + (2. * roc(source, period_roc_second).smooth(smooth, period_second))
        + (3. * roc(source, period_roc_third).smooth(smooth, period_third))
        + (4. * roc(source, period_roc_fouth).smooth(smooth, period_fouth))
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
            0.0, 0.0, 0.0, 0.0, 0.0, 3.2460651, 5.4379296, 7.731903, 8.935576, 9.378514, 9.048229,
            8.414183,
        ];

        let result: Vec<Scalar> = kst(
            &source,
            Smooth::SMA,
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
