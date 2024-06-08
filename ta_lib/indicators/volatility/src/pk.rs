use core::prelude::*;

pub fn pk(high: &Series<f32>, low: &Series<f32>, period: usize) -> Series<f32> {
    let hll = (high / low).log();

    let factor = 1. / (4.0 * period as f32 * 2.0_f32.ln());

    let hls = factor * hll.pow(2).sum(period);

    hls.sqrt()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parkinson() {
        let high = Series::from([1.0, 2.0, 3.0, 2.0, 5.0]);
        let low = Series::from([3.0, 2.0, 3.0, 4.0, 5.0]);
        let period = 3;

        let expected = vec![0.38092643, 0.38092643, 0.38092643, 0.24033782, 0.24033782];

        let result: Vec<f32> = pk(&high, &low, period).into();

        assert_eq!(result, expected);
    }
}
