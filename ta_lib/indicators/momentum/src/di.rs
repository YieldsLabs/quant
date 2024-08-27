use core::prelude::*;

pub fn di(source: &Price, smooth_type: Smooth, period: Period) -> Price {
    let ma = source.smooth(smooth_type, period);

    SCALE * (source - &ma) / ma
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_di() {
        let source = Series::from([
            6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365, 6.8310, 6.8355,
            6.8360, 6.8345, 6.8285, 6.8395,
        ]);
        let expected = vec![
            -0.0000069530056,
            0.009725365,
            -0.08268177,
            0.040116996,
            0.07046368,
            -0.038874596,
            -0.0985024,
            -0.030419156,
            -0.06334749,
            -0.0609653,
            0.01951538,
            0.01462254,
            -0.009752775,
            -0.04756681,
            0.0658433,
        ];

        let result: Vec<Scalar> = di(&source, Smooth::WMA, 3).into();

        assert_eq!(result, expected);
    }
}
