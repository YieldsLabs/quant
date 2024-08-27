use crate::constants::{ONE, PI, SCALE, ZERO};
use crate::series::Series;
use crate::traits::Comparator;
use crate::types::{Period, Price, Scalar};
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
    DEMA,
    ULTS,
}

impl Price {
    pub fn ew(&self, alpha: &Price, seed: &Price) -> Self {
        let len = self.len();
        let mut sum = Series::zero(len);
        let a = alpha * self;
        let b = ONE - alpha;

        for _ in 0..len {
            sum = &a + &b * nz!(sum.shift(1), seed)
        }

        sum
    }

    pub fn wg(&self, weights: &[Scalar]) -> Self {
        let mut sum = Series::zero(self.len());
        let norm = weights.iter().sum::<Scalar>();

        for (i, &weight) in weights.iter().enumerate() {
            sum = sum + nz!(self.shift(i), self) * weight;
        }

        sum / norm
    }

    fn ema(&self, period: Period) -> Self {
        let alpha = Series::fill(2. / (period + 1) as Scalar, self.len());

        self.ew(&alpha, self)
    }

    fn smma(&self, period: Period) -> Self {
        let alpha = Series::fill(ONE / (period as Scalar), self.len());
        let seed = self.ma(period);

        self.ew(&alpha, &seed)
    }

    fn dema(&self, period: Period) -> Self {
        let ema = self.ema(period);

        2. * &ema - ema.ema(period)
    }

    fn tema(&self, period: Period) -> Self {
        let ema1 = self.ema(period);
        let ema2 = ema1.ema(period);
        let ema3 = ema2.ema(period);

        3. * (ema1 - ema2) + ema3
    }

    fn wma(&self, period: Period) -> Self {
        let weights = (0..period)
            .map(|i| (period - i) as Scalar)
            .collect::<Vec<_>>();

        self.wg(&weights)
    }

    fn swma(&self) -> Self {
        let x1 = nz!(self.shift(1), self);
        let x2 = nz!(self.shift(2), self);
        let x3 = nz!(self.shift(3), self);

        x3 * ONE / 6. + x2 * 2. / 6. + x1 * 2. / 6. + self * ONE / 6.
    }

    fn hma(&self, period: Period) -> Self {
        let lag = (0.5 * period as Scalar) as Period;
        let sqrt_period = (period as Scalar).sqrt().floor() as Period;

        (2. * self.wma(lag) - self.wma(period)).wma(sqrt_period)
    }

    fn linreg(&self, period: Period) -> Self {
        let x = (0..self.len()).map(|i| i as Scalar).collect::<Series<_>>();

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

    fn kama(&self, period: Period) -> Self {
        let len = self.len();
        let mom = self.change(period).abs();
        let volatility = self.change(1).abs().sum(period);
        let er = iff!(volatility.seq(&ZERO), Series::zero(len), mom / volatility);

        let alpha = (er.nz(Some(ZERO)) * 0.6015 + 0.0645).pow(2);

        self.ew(&alpha, self)
    }

    fn zlema(&self, period: Period) -> Self {
        let lag = (0.5 * (period - 1) as Scalar).floor() as Period;

        (self + (self - nz!(self.shift(lag), self))).ema(period)
    }

    fn ults(&self, period: Period) -> Self {
        let a1 = (-1.414 * PI / period as Scalar).exp();
        let c2 = 2. * a1 * (1.414 * PI / period as Scalar).cos();
        let c3 = -a1 * a1;
        let c1 = 0.25 * (ONE + c2 - c3);

        let len = self.len();

        let mut us = Series::zero(len);

        let src1 = nz!(self.shift(1), self);
        let src2 = nz!(self.shift(2), src1);

        let a = (ONE - c1) * self;
        let b = (2. * c1 - c2) * &src1;
        let c = (c1 + c3) * &src2;

        let abc = a + b - c;

        for _ in 0..len {
            let d = c2 * nz!(us.shift(1), src1);
            let e = c3 * nz!(us.shift(2), src2);

            us = &abc + d + e;
        }

        us
    }

    pub fn smooth(&self, smooth: Smooth, period: Period) -> Self {
        match smooth {
            Smooth::EMA => self.ema(period),
            Smooth::SMA => self.ma(period),
            Smooth::SMMA => self.smma(period),
            Smooth::KAMA => self.kama(period),
            Smooth::HMA => self.hma(period),
            Smooth::WMA => self.wma(period),
            Smooth::ZLEMA => self.zlema(period),
            Smooth::LSMA => self.linreg(period),
            Smooth::TEMA => self.tema(period),
            Smooth::DEMA => self.dema(period),
            Smooth::ULTS => self.ults(period),
        }
    }

    pub fn spread(&self, smooth: Smooth, period_fast: Period, period_slow: Period) -> Self {
        self.smooth(smooth, period_fast) - self.smooth(smooth, period_slow)
    }

    pub fn spread_pct(&self, smooth: Smooth, period_fast: Period, period_slow: Period) -> Self {
        let fsm = self.smooth(smooth, period_fast);
        let ssm = self.smooth(smooth, period_slow);

        SCALE * (fsm - &ssm) / &ssm
    }

    pub fn spread_diff(
        &self,
        smooth: Smooth,
        period_fast: Period,
        period_slow: Period,
        n: usize,
    ) -> Self {
        self.spread(smooth, period_fast, period_slow)
            - self.shift(n).spread(smooth, period_fast, period_slow)
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
        let expected = Series::from([1.0, 1.6666666, 2.3333333, 3.3333333, 4.3333335]);

        let result = source.wma(3);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_swma() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([1.0, 1.6666667, 2.0, 2.5, 3.5]);

        let result = source.swma();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_kama() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([1.0, 1.0041603, 1.0124636, 2.337603, 3.5185251]);

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

    #[test]
    fn test_ults() {
        let source = Series::from([
            0.3847, 0.3863, 0.3885, 0.3839, 0.3834, 0.3843, 0.3840, 0.3834, 0.3832,
        ]);
        let expected = Series::from([
            0.38469997, 0.38586292, 0.3883182, 0.3857727, 0.38236603, 0.38377836, 0.38435996,
            0.38352367, 0.38307717,
        ]);

        let result = source.ults(3);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_spread() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([0.0, 0.16666675, 0.30555558, 0.39351845, 0.44367313]);
        let period_fast = 2;
        let period_slow = 3;
        let smooth = Smooth::EMA;

        let result = source.spread(smooth, period_fast, period_slow);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_percent_of_spread() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([0.0, 11.111117, 13.580248, 12.59259, 10.921185]);
        let period_fast = 2;
        let period_slow = 3;
        let smooth = Smooth::EMA;

        let result = source.spread_pct(smooth, period_fast, period_slow);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_spread_diff() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([f32::NAN, 0.16666675, 0.13888884, 0.087962866, 0.050154686]);
        let period_fast = 2;
        let period_slow = 3;
        let n = 1;
        let smooth = Smooth::EMA;

        let result = source.spread_diff(smooth, period_fast, period_slow, n);

        assert_eq!(result, expected);
    }
}
