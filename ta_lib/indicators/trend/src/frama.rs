use core::prelude::*;

pub fn frama(source: &Price, high: &Price, low: &Price, period: Period) -> Price {
    let len = (0.5 * period as Scalar).floor() as Period;
    let hh = high.highest(len);
    let ll = low.lowest(len);

    let n1 = (&hh - &ll) / len as Scalar;
    let n2 = (hh.shift(len) - ll.shift(len)) / len as Scalar;
    let n3 = (high.highest(period) - low.lowest(period)) / period as Scalar;

    let d = ((n1 + n2) / n3).log() / 2.0_f32.ln();

    let alpha = (-4.6 * (d - 1.)).exp();

    source.ew(&alpha, source)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_frama() {
        let high = Series::from([
            5.0994, 5.0910, 5.1015, 5.1051, 5.1041, 5.1138, 5.1150, 5.1160, 5.1392, 5.1550, 5.1739,
            5.2000, 5.2193,
        ]);
        let low = Series::from([
            5.0770, 5.0788, 5.0897, 5.0933, 5.0943, 5.0996, 5.1001, 5.0968, 5.1125, 5.1326, 5.1468,
            5.1675, 5.1907,
        ]);
        let source = Series::from([
            5.0788, 5.0897, 5.0958, 5.1023, 5.0998, 5.1046, 5.1014, 5.1141, 5.1355, 5.1477, 5.1675,
            5.2000, 5.2169,
        ]);
        let expected = vec![
            0.0, 5.0896997, 5.090174, 5.0918617, 5.0919185, 5.092221, 5.092286, 5.092319, 5.094049,
            5.105295, 5.122919, 5.1347446, 5.152087,
        ];

        let result: Vec<Scalar> = frama(&source, &high, &low, 3).into();

        assert_eq!(result, expected);
    }
}
