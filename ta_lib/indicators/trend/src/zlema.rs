use core::prelude::*;

pub fn zlema(source: &Series<f32>, period: usize) -> Series<f32> {
    let lag = ((period as f32 - 1.) / 2.) as usize;

    let d = (2. * source) - source.shift(lag);

    d.ema(period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zlema() {
        let source = Series::from([18.898, 18.838, 18.881, 18.925, 18.846]);
        let period = 3;
        let expected = vec![0.0, 18.777998, 18.851, 18.91, 18.838501];

        let result: Vec<f32> = zlema(&source, period).into();

        assert_eq!(result, expected);
    }
}
