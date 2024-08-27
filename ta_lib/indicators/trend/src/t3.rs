use core::prelude::*;

pub fn t3(source: &Price, period: Period) -> Price {
    let alpha = 0.618;

    let ema1 = source.smooth(Smooth::EMA, period);
    let ema2 = ema1.smooth(Smooth::EMA, period);
    let ema3 = ema2.smooth(Smooth::EMA, period);
    let ema4 = ema3.smooth(Smooth::EMA, period);
    let ema5 = ema4.smooth(Smooth::EMA, period);
    let ema6 = ema5.smooth(Smooth::EMA, period);

    let form1 = -alpha * alpha * alpha;
    let form2 = 3. * alpha * alpha + 3. * alpha * alpha * alpha;
    let form3 = -6. * alpha * alpha - 3. * alpha - 3. * alpha * alpha * alpha;
    let form4 = 1. + 3. * alpha + alpha * alpha * alpha + 3. * alpha * alpha;

    form1 * ema6 + form2 * ema5 + form3 * ema4 + form4 * ema3
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_t3() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = vec![1.0, 1.2803686, 1.8820143, 2.717381, 3.6838531];

        let result: Vec<Scalar> = t3(&source, 3).into();

        assert_eq!(result, expected);
    }
}
