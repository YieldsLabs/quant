use crate::series::Series;
use crate::traits::Comparator;
use crate::ZERO;
use crate::{iff, nz};

#[derive(Copy, Clone)]
pub enum Smooth {
    EMA,
    SMA,
    SMMA,
    KAMA,
    HMA,
    WMA,
    ZLEMA,
    LSMA,
    TEMA,
}

impl Series<f32> {
    pub fn ew(&self, alpha: &Series<f32>, seed: &Series<f32>) -> Self {
        let len = self.len();
        let mut sum = Series::zero(len);

        for _ in 0..len {
            sum = alpha * self + (1. - alpha) * nz!(sum.shift(1), seed)
        }

        sum
    }

    pub fn wg(&self, weights: &[f32]) -> Self {
        let mut sum = Series::zero(self.len());
        let norm = weights.iter().sum::<f32>();

        for (i, &weight) in weights.iter().enumerate() {
            sum = sum + self.shift(i) * weight;
        }

        sum / norm
    }

    fn ema(&self, period: usize) -> Self {
        let alpha = Series::fill(2. / (period as f32 + 1.), self.len());

        self.ew(&alpha, self)
    }

    fn smma(&self, period: usize) -> Self {
        let alpha = Series::fill(1. / (period as f32), self.len());
        let seed = self.ma(period);

        self.ew(&alpha, &seed)
    }

    fn tema(&self, period: usize) -> Self {
        let ema1 = self.ema(period);
        let ema2 = ema1.ema(period);
        let ema3 = ema2.ema(period);

        3. * (ema1 - ema2) + ema3
    }

    fn wma(&self, period: usize) -> Self {
        let weights = (0..period).map(|i| (period - i) as f32).collect::<Vec<_>>();

        self.wg(&weights)
    }

    fn swma(&self) -> Self {
        let x1 = self.shift(1);
        let x2 = self.shift(2);
        let x3 = self.shift(3);

        x3 * 1. / 6. + x2 * 2. / 6. + x1 * 2. / 6. + self * 1. / 6.
    }

    fn hma(&self, period: usize) -> Self {
        let lag = (0.5 * period as f32).round() as usize;
        let sqrt_period = (period as f32).sqrt() as usize;

        (2. * self.wma(lag) - self.wma(period)).wma(sqrt_period)
    }

    fn linreg(&self, period: usize) -> Self {
        let x = (0..self.len()).map(|i| i as f32).collect::<Series<_>>();

        let x_mean = x.ma(period);
        let y_mean = self.ma(period);

        let xy = &x * self;
        let xx = &x.pow(2);

        let xy_ma = xy.ma(period);
        let xx_ma = xx.ma(period);

        let slope = (&xy_ma - &x_mean * &y_mean) / (&xx_ma - &x_mean * &x_mean);

        let intercept = &y_mean - &slope * &x_mean;

        &intercept + &slope * &x
    }

    fn kama(&self, period: usize) -> Series<f32> {
        let len = self.len();
        let mom = self.change(period).abs();
        let volatility = self.change(1).abs().sum(period);
        let er = iff!(volatility.seq(&ZERO), Series::zero(len), mom / volatility);

        let alpha = (er * 0.666_666_7).pow(2);

        self.ew(&alpha, self)
    }

    fn zlema(&self, period: usize) -> Series<f32> {
        let lag = (0.5 * (period as f32 - 1.)) as usize;

        (self + (self - self.shift(lag))).ema(period)
    }

    pub fn smooth(&self, smooth_type: Smooth, period: usize) -> Self {
        match smooth_type {
            Smooth::EMA => self.ema(period),
            Smooth::SMA => self.ma(period),
            Smooth::SMMA => self.smma(period),
            Smooth::KAMA => self.kama(period),
            Smooth::HMA => self.hma(period),
            Smooth::WMA => self.wma(period),
            Smooth::ZLEMA => self.zlema(period),
            Smooth::LSMA => self.linreg(period),
            Smooth::TEMA => self.tema(period),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ema() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([1.0, 1.5, 2.25, 3.125, 4.0625]);

        let result = source.ema(3);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_smma() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([1.0, 1.3333333, 1.8888888, 2.5925925, 3.3950615]);

        let result = source.smma(3);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_wma() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([f32::NAN, f32::NAN, 2.3333333, 3.3333333, 4.3333335]);

        let result = source.wma(3);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_swma() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([f32::NAN, f32::NAN, f32::NAN, 2.5, 3.5]);

        let result = source.swma();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_kama() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([f32::NAN, f32::NAN, f32::NAN, 4.0, 4.4444447]);

        let result = source.kama(3);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_linreg() {
        let source = Series::from([
            7.1135, 7.088, 7.112, 7.1205, 7.1195, 7.136, 7.1405, 7.112, 7.1095, 7.1220, 7.1310,
            7.1550, 7.1480, 7.1435, 7.1405, 7.1440, 7.1495, 7.1515, 7.1415, 7.1445, 7.1525, 7.1440,
            7.1370, 7.1305, 7.1375, 7.1250, 7.1190, 7.1135, 7.1280, 7.1220, 7.1230, 7.1225, 7.1180,
            7.1250, 7.1230, 7.1130, 7.1210, 7.13, 7.134, 7.132, 7.116, 7.1235, 7.1645, 7.1565,
            7.1560,
        ]);

        let expected = Series::from([
            7.1135, 7.088, 7.10375, 7.1230836, 7.121082, 7.133084, 7.1425056, 7.117501, 7.1051655,
            7.1194954, 7.13158, 7.152491, 7.1531696, 7.143088, 7.140269, 7.142896, 7.1491756,
            7.1520867, 7.1434836, 7.1423316, 7.15166, 7.146748, 7.136764, 7.1304145, 7.1352515,
            7.1282535, 7.117897, 7.113399, 7.124653, 7.125424, 7.121816, 7.122751, 7.118672,
            7.1230693, 7.124495, 7.114359, 7.1180387, 7.1298475, 7.1348333, 7.133007, 7.1183147,
            7.1196218, 7.15893, 7.164693, 7.1547427,
        ]);

        let result = source.linreg(3);

        assert_eq!(result.len(), expected.len());
        assert_eq!(result, expected);
    }
}
