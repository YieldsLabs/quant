use crate::iff;
use crate::series::Series;

impl Series<f32> {
    pub fn ew(&self, alpha: &Series<f32>, seed: &Series<f32>) -> Self {
        let mut sum = Series::empty(self.len());

        for _ in 0..self.len() {
            let prev = sum.shift(1);

            sum = iff!(
                prev.na(),
                seed,
                alpha * self + (1. - alpha) * prev.nz(Some(0.))
            )
        }

        sum
    }

    pub fn ma(&self, period: usize) -> Self {
        self.sliding_map(period, |window, size, _| {
            Some(window.iter().flatten().sum::<f32>() / size)
        })
    }

    pub fn ema(&self, period: usize) -> Self {
        let alpha = Series::fill(2. / (period as f32 + 1.), self.len());

        self.ew(&alpha, self)
    }

    pub fn smma(&self, period: usize) -> Self {
        let alpha = Series::fill(1. / (period as f32), self.len());

        self.ew(&alpha, &self.ma(period))
    }

    pub fn wma(&self, period: usize) -> Self {
        let mut sum = Series::zero(self.len());
        let mut norm = 0.;

        for i in 0..period {
            let weight = (period - i) as f32;

            norm += weight;
            sum = sum + self.shift(i) * weight;
        }

        sum / norm
    }

    pub fn swma(&self) -> Self {
        let x1 = self.shift(1);
        let x2 = self.shift(2);
        let x3 = self.shift(3);

        x3 * 1. / 6. + x2 * 2. / 6. + x1 * 2. / 6. + self * 1. / 6.
    }

    pub fn hma(&self, period: usize) -> Self {
        let lag = (period as f32 / 2.).round() as usize;
        let sqrt_period = (period as f32).sqrt() as usize;

        (2. * self.wma(lag) - self.wma(period)).wma(sqrt_period)
    }

    pub fn linreg(&self, period: usize) -> Self {
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
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ma() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = Series::from([1.0, 1.5, 2.0, 3.0, 4.0]);

        let result = source.ma(3);

        assert_eq!(result, expected);
    }

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
    fn test_linreg() {
        let source = Series::from([
            7.1135, 7.088, 7.112, 7.1205, 7.1195, 7.136, 7.1405, 7.112, 7.1095, 7.1220, 7.1310,
            7.1550, 7.1480, 7.1435, 7.1405, 7.1440, 7.1495, 7.1515, 7.1415, 7.1445, 7.1525, 7.1440,
            7.1370, 7.1305, 7.1375, 7.1250, 7.1190, 7.1135, 7.1280, 7.1220, 7.1230, 7.1225, 7.1180,
            7.1250, 7.1230, 7.1130, 7.1210, 7.13, 7.134, 7.132, 7.116, 7.1235, 7.1645, 7.1565,
            7.1560,
        ]);

        let expected = Series::from([
            f32::NAN,
            7.088,
            7.10375,
            7.1230836,
            7.1210837,
            7.133084,
            7.1425,
            7.117501,
            7.1051655,
            7.1194954,
            7.1315904,
            7.152491,
            7.1531696,
            7.1430774,
            7.140269,
            7.1429076,
            7.1491756,
            7.1520867,
            7.1434836,
            7.1423316,
            7.15166,
            7.146748,
            7.136764,
            7.1304145,
            7.1352515,
            7.1282535,
            7.117897,
            7.113399,
            7.124653,
            7.125424,
            7.121861,
            7.122751,
            7.118672,
            7.1230693,
            7.124495,
            7.114359,
            7.118015,
            7.129894,
            7.1348333,
            7.133007,
            7.1183147,
            7.1196218,
            7.15893,
            7.164693,
            7.1547427,
        ]);

        let result = source.linreg(3);

        assert_eq!(result, expected);
    }
}
