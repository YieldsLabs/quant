use core::prelude::*;

pub fn cmo(source: &Series<f32>, period: usize) -> Series<f32> {
    let mom = source.change(1);
    let zero = Series::zero(source.len());

    let hcls = iff!(mom.sgte(&ZERO), mom, zero);
    let lcls = iff!(mom.slte(&ZERO), mom.negate(), zero);

    let hsum = hcls.sum(period);
    let lsum = lcls.sum(period);

    SCALE * (&hsum - &lsum) / (&hsum + &lsum)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cmo() {
        let close = Series::from([19.571, 19.606, 19.594, 19.575, 19.612, 19.631, 19.634]);
        let expected = vec![0.0, 100.0, 48.934788, 6.062883, 8.821632, 49.33496, 100.0];

        let result: Vec<f32> = cmo(&close, 3).into();

        assert_eq!(result, expected);
    }
}
