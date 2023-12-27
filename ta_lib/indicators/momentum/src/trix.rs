use core::prelude::*;

const PERCENTAGE_SCALE: f32 = 100.;

pub fn trix(source: &Series<f32>, period: usize) -> Series<f32> {
    let ema3 = source.ema(period).ema(period).ema(period);

    PERCENTAGE_SCALE.powf(2.0) * (&ema3 / ema3.shift(1) - 1.)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_trix() {
        let source = Series::from([
            6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365, 6.8310, 6.8355,
            6.8360, 6.8345, 6.8285, 6.8395,
        ]);
        let period = 3;
        let expected = vec![
            0.0, 0.36478043, -1.6403198, -1.0019541, 0.9572506, 0.61511993, -1.92523, -3.3217669,
            -5.0127506, -6.273389, -5.246997, -3.7002563, -2.6726723, -2.9873848, -0.9274483,
        ];

        let result: Vec<f32> = trix(&source, period).into();

        assert_eq!(result, expected);
    }
}
