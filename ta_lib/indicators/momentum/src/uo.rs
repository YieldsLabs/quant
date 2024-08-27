use core::prelude::*;

pub fn uo(
    source: &Price,
    high: &Price,
    low: &Price,
    period_fast: Period,
    period_medium: Period,
    period_slow: Period,
) -> Price {
    let prev_source = source.shift(1).nz(Some(0.0));

    let high = prev_source.max(high);
    let low = prev_source.min(low);

    let bp = source - &low;
    let tr = high - &low;

    100. * (4. * bp.sum(period_fast) / tr.sum(period_fast)
        + 2. * bp.sum(period_medium) / tr.sum(period_medium)
        + bp.sum(period_slow) / tr.sum(period_slow))
        / 7.
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_uo() {
        let source = Series::from([
            6.6430, 6.8595, 6.8680, 6.8650, 6.8445, 6.8560, 6.8565, 6.8590, 6.8530, 6.8575, 6.855,
            6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365, 6.8310, 6.8355,
            6.8360, 6.8345, 6.8285, 6.8395,
        ]);
        let high = Series::from([
            6.8430, 6.8660, 6.8685, 6.8690, 6.865, 6.8595, 6.8565, 6.862, 6.859, 6.86, 6.8580,
            6.8605, 6.8620, 6.86, 6.859, 6.8670, 6.8640, 6.8575, 6.8485, 6.8450, 6.8365, 6.84,
            6.8385, 6.8365, 6.8345, 6.8395,
        ]);
        let low = Series::from([
            6.8380, 6.8430, 6.8595, 6.8640, 6.8435, 6.8445, 6.8510, 6.8560, 6.8520, 6.8530, 6.8550,
            6.8550, 6.8565, 6.8475, 6.8480, 6.8535, 6.8565, 6.8455, 6.8445, 6.8365, 6.8310, 6.8310,
            6.8345, 6.8325, 6.8275, 6.8285,
        ]);
        let expected = vec![
            97.07731, 97.07755, 97.02184, 79.879684, 25.307936, 35.087112, 65.40703, 70.05135,
            41.210888, 42.434715, 40.23762, 39.388878, 54.514324, 24.983133, 44.44906, 70.54365,
            53.009586, 15.58435, 6.6393533, 3.0904624, 1.0311968, 25.968098, 38.813465, 43.52247,
            29.511023, 64.793076,
        ];
        let period_fast = 2;
        let period_medium = 3;
        let period_slow = 4;

        let result: Vec<Scalar> = uo(
            &source,
            &high,
            &low,
            period_fast,
            period_medium,
            period_slow,
        )
        .into();

        assert_eq!(result, expected);
    }
}
