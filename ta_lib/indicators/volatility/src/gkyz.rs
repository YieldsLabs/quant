use core::prelude::*;

pub fn gkyz(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
    period: usize,
) -> Series<f32> {
    let gkyzl = (open / close.shift(1).nz(Some(ZERO))).log();
    let pkl = (high / low).log();
    let gkl = (close / open).log();
    let gm = 2.0 * 2.0_f32.ln() - 1.0;

    let gkyzs = (1.0 / period as f32) * gkyzl.pow(2).sum(period);
    let pks = (1.0 / (2.0 * period as f32)) * pkl.pow(2).sum(period);
    let gs = (gm / period as f32) * gkl.pow(2).sum(period);

    (gkyzs + pks - gs).sqrt()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_garman_klass_yang_zhang() {
        let open = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let high = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let low = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let close = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let period = 3;

        let expected = vec![0.0, 0.4001887, 0.4636288, 0.49248216, 0.31461933];

        let result: Vec<f32> = gkyz(&open, &high, &low, &close, period).into();

        assert_eq!(result, expected);
    }
}
