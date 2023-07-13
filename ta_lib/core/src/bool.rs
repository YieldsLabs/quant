use crate::series::Series;

impl Series<f64> {
    pub fn eq(&self, scalar: f64) -> Series<bool> {
        self.fmap(|x| x.map(|v| *v == scalar))
    }

    pub fn ne(&self, scalar: f64) -> Series<bool> {
        self.fmap(|x| x.map(|v| *v != scalar))
    }

    pub fn gt(&self, scalar: f64) -> Series<bool> {
        self.fmap(|x| x.map(|v| *v > scalar))
    }

    pub fn gte(&self, scalar: f64) -> Series<bool> {
        self.fmap(|x| x.map(|v| *v >= scalar))
    }

    pub fn lt(&self, scalar: f64) -> Series<bool> {
        self.fmap(|x| x.map(|v| *v < scalar))
    }

    pub fn lte(&self, scalar: f64) -> Series<bool> {
        self.fmap(|x| x.map(|v| *v <= scalar))
    }
}
