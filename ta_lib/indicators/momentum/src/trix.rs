use crate::roc;
use core::prelude::*;

const SCALE: f32 = 1.;

pub fn trix(source: &Series<f32>, period: usize) -> Series<f32> {
    let ema3 = source
        .smooth(Smooth::EMA, period)
        .smooth(Smooth::EMA, period)
        .smooth(Smooth::EMA, period);

    SCALE * roc(&ema3, 1)
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
            0.0,
            0.0036433754,
            -0.016401544,
            -0.010020561,
            0.009569516,
            0.0061472696,
            -0.019254234,
            -0.0332163,
            -0.050126247,
            -0.06273622,
            -0.05246739,
            -0.0370036,
            -0.026727742,
            -0.029872786,
            -0.009277002,
        ];

        let result: Vec<f32> = trix(&source, period).into();

        assert_eq!(result, expected);
    }
}
