use crate::rs;
use core::prelude::*;

pub fn yz(open: &Price, high: &Price, low: &Price, close: &Price, period: Period) -> Price {
    let oc = (open / close.shift(1).nz(Some(ZERO))).log();
    let ochat = oc.ma(period);

    let co = (close / open).log();
    let cohat = co.ma(period);

    let factor = 1. / (period - 1) as Scalar;

    let ov = factor * (oc - ochat).pow(2).sum(period);
    let oc = factor * (co - cohat).pow(2).sum(period);

    let k = 0.34 / (1.34 + (period + 1) as Scalar / (period - 1) as Scalar);
    let rs = rs(open, high, low, close, period).pow(2);

    (ov + k * oc + (1. - k) * rs).sqrt()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_yang_zhang() {
        let open = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let high = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let low = Series::from([3.0, 2.0, 3.0, 4.0, 5.0]);
        let close = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let period = 3;

        let expected = vec![0.0, 0.64916766, 0.649761, 0.27574953, 0.13916442];

        let result: Vec<Scalar> = yz(&open, &high, &low, &close, period).into();

        assert_eq!(result, expected);
    }
}
