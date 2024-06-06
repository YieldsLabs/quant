use core::prelude::*;

pub fn rs(
    open: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
    period: usize,
) -> Series<f32> {
    let hl = (high / close).log() * (high / open).log();
    let ll = (low / close).log() * (low / open).log();
    let factor = 1.0 / period as f32;

    let hs = factor * hl.sum(period);
    let ls = factor * ll.sum(period);

    (hs + ls).sqrt()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rogers_satchell() {
        let open = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let high = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let low = Series::from([3.0, 2.0, 3.0, 4.0, 5.0]);
        let close = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let period = 3;

        let expected = vec![0.63428414, 0.63428414, 0.63428414, 0.0, 0.0];

        let result: Vec<f32> = rs(&open, &high, &low, &close, period).into();

        assert_eq!(result, expected);
    }
}
