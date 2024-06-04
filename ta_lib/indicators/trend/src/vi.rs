use core::prelude::*;

pub fn vi(
    high: &Series<f32>,
    low: &Series<f32>,
    atr: &Series<f32>,
    period: usize,
) -> (Series<f32>, Series<f32>) {
    let vmp = (high - low.shift(1)).abs().sum(period);
    let vmm = (low - high.shift(1)).abs().sum(period);
    let atrs = atr.sum(period);

    (vmp / &atrs, vmm / &atrs)
}

#[cfg(test)]
mod tests {
    use super::*;
    use volatility::atr;

    #[test]
    fn test_vi() {
        let high = Series::from([
            9.682, 9.684, 9.680, 9.664, 9.663, 9.660, 9.669, 9.670, 9.675, 9.659, 9.651,
        ]);
        let low = Series::from([
            9.672, 9.679, 9.663, 9.646, 9.653, 9.655, 9.652, 9.643, 9.659, 9.644, 9.634,
        ]);
        let close = Series::from([
            9.682, 9.680, 9.663, 9.663, 9.656, 9.659, 9.656, 9.670, 9.659, 9.646, 9.640,
        ]);
        let atr_period = 1;
        let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);
        let expected_vip = vec![
            0.0,
            0.79998726,
            0.5909229,
            0.057138965,
            0.6428474,
            1.5999745,
            0.9545691,
            0.7272688,
            1.1627891,
            1.0322709,
            0.21874535,
        ];
        let expected_vim = vec![
            0.0, 0.20001271, 1.0909013, 1.5714442, 1.6071526, 1.2666413, 0.72728455, 0.7727204,
            0.8604538, 1.3548268, 1.7499926,
        ];

        let (vip, vim) = vi(&high, &low, &atr, 2);
        let vvip: Vec<f32> = vip.into();
        let vvim: Vec<f32> = vim.into();

        assert_eq!(vvip, expected_vip);
        assert_eq!(vvim, expected_vim);
    }
}
