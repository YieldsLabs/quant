use core::prelude::*;

const SCALE: f32 = 1000.;

pub fn tdfi(source: &Series<f32>, smooth_type: Smooth, period: usize, n: usize) -> Series<f32> {
    let ma = (SCALE * source).smooth(smooth_type, period);
    let sma = ma.smooth(smooth_type, period);

    let tdf = (&ma - &sma).abs().pow(1) * (0.5 * (ma.change(1) + sma.change(1))).pow(n);

    &tdf / tdf.abs().highest(period * n)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tdfi() {
        let source = Series::from([
            11.305, 11.285, 11.278, 11.240, 11.247, 11.209, 11.230, 11.242, 11.221, 11.176, 11.176,
            11.161, 11.192, 11.207, 11.197, 11.186,
        ]);
        let period = 3;
        let n = 2;
        let smooth_type = Smooth::EMA;
        let expected = vec![
            0.0,
            1.0,
            1.0,
            1.0,
            0.2042108,
            1.0,
            0.033832937,
            0.0008659027,
            0.026829286,
            0.97299135,
            0.38781586,
            0.4164741,
            0.0032546856,
            0.04190661,
            0.0011795466,
            0.0041924296,
        ];

        let result: Vec<f32> = tdfi(&source, smooth_type, period, n).into();

        assert_eq!(result, expected);
    }
}
