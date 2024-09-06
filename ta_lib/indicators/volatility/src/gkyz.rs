use core::prelude::*;

pub fn gkyz(open: &Price, high: &Price, low: &Price, close: &Price, period: Period) -> Price {
    let gkyzl = (open / close.shift(1).nz(Some(ZERO))).log();
    let pkl = (high / low).log();
    let gkl = (close / open).log();
    let gm = 2.0 * 2.0_f32.ln() - 1.0;

    let gkyzs = (1.0 / period as Scalar) * gkyzl.pow(2).sum(period);
    let pks = (1.0 / (2.0 * period as Scalar)) * pkl.pow(2).sum(period);
    let gs = (gm / period as Scalar) * gkl.pow(2).sum(period);

    (gkyzs + pks - gs).sqrt()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_garman_klass_yang_zhang() {
        let open = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let high = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let low = Series::from([3.0, 2.0, 3.0, 4.0, 5.0]);
        let close = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let period = 3;

        let expected = vec![0.0, 0.60109, 0.6450658, 0.49248216, 0.31461933];

        let result: Vec<Scalar> = gkyz(&open, &high, &low, &close, period).into();

        assert_eq!(result, expected);
    }
}
